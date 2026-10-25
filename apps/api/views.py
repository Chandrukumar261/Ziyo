import hmac
import hashlib
import json
from decimal import Decimal
from django.db import transaction
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from rest_framework import status, views, permissions
from rest_framework.response import Response

from apps.catalog.models import Product, ProductVariant
from apps.inventory.models import InventoryItem, StockMovement, InsufficientStockError
from apps.orders.models import Order, OrderItem, OrderStatusHistory, Shipment
from apps.payments.models import Payment
from apps.payments.razorpay_service import RazorpayService
from apps.cart.cart_service import get_or_create_cart, calculate_cart_totals
from apps.cart.models import Cart, CartItem
from apps.core.models import AuditLog

from .permissions import IsStaffOrManager
from .serializers import (
    ProductSerializer,
    CartItemInputSerializer,
    CheckoutOrderCreateSerializer,
    OrderDetailSerializer,
    PaymentVerificationSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    InventoryAdjustSerializer,
    OrderStatusUpdateSerializer,
    CustomerOrderListSerializer,
    CustomerOrderDetailSerializer,
    OrderLiveTrackingSerializer,
    OrderShippingAddressUpdateSerializer,
    ErpBulkInventorySyncSerializer,
    LogisticsDispatchSerializer,
    ErpGenericWebhookSerializer,
)

# ==============================================================================
# 1. CHECKOUT & PAYMENT SECURITY API
# ==============================================================================

class CheckoutOrderCreateAPIView(views.APIView):
    """
    POST /api/v1/checkout/order/
    Server-authoritative checkout creation.
    Validates cart, looks up prices from DB, executes atomic stock reservation,
    and initiates Razorpay gateway order.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CheckoutOrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart = get_or_create_cart(request)
        cart_totals = calculate_cart_totals(cart, request)

        if cart_totals["total_items"] == 0:
            return Response(
                {"error": "Cart is empty. Please add items before checking out."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data

        try:
            with transaction.atomic():
                # Concurrency defense: lock inventory rows and verify stock
                for item in cart_totals["items"]:
                    if hasattr(item.product, "inventory"):
                        # Lock inventory row
                        inv = InventoryItem.objects.select_for_update().get(id=item.product.inventory.id)
                        if inv.available_quantity < item.quantity:
                            raise InsufficientStockError(
                                f"Insufficient stock for {item.product.name}. Available: {inv.available_quantity}"
                            )

                payment_method = data.get("payment_method", "RAZORPAY_CARD")

                # Create authoritative order with DB prices
                order = Order.objects.create(
                    order_number=Order.generate_order_number(),
                    user=request.user if request.user.is_authenticated else None,
                    email=data["email"],
                    phone=data["phone"],
                    status=Order.Status.PROCESSING if payment_method == "COD" else Order.Status.PAYMENT_PENDING,
                    subtotal=cart_totals["subtotal"],
                    discount_amount=cart_totals["discount_amount"],
                    coupon_code=cart_totals["coupon_code"],
                    shipping_fee=cart_totals["shipping_fee"],
                    tax_amount=cart_totals["tax_amount"],
                    total_amount=cart_totals["total"],
                    shipping_full_name=data["full_name"],
                    shipping_phone=data["phone"],
                    shipping_address_line_1=data["address_line_1"],
                    shipping_address_line_2=data.get("address_line_2", ""),
                    shipping_city=data["city"],
                    shipping_state=data["state"],
                    shipping_postal_code=data["postal_code"],
                    shipping_country=data.get("country", "India"),
                    customer_notes=data.get("customer_notes", ""),
                )

                # Persist snapshot line items with strictly server-verified prices
                for item in cart_totals["items"]:
                    unit_p = item.current_price
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        product_name=item.product.name,
                        variant_name=item.variant.name if item.variant else "",
                        sku=item.variant.sku if item.variant else item.product.sku,
                        unit_price=unit_p,
                        quantity=item.quantity,
                        line_total=unit_p * item.quantity,
                    )
                    # Hold stock
                    if hasattr(item.product, "inventory"):
                        item.product.inventory.reserve_stock(
                            quantity=item.quantity,
                            reference_id=order.order_number,
                        )

                if payment_method == "COD":
                    RazorpayService.finalize_cod_order(order)
                    cart.items.all().delete()
                    return Response(
                        {
                            "order_id": str(order.id),
                            "order_number": order.order_number,
                            "total_amount": str(order.total_amount),
                            "currency": "INR",
                            "payment_method": "COD",
                            "status": order.status,
                            "message": "Order placed successfully with Cash on Delivery.",
                        },
                        status=status.HTTP_201_CREATED,
                    )

                OrderStatusHistory.objects.create(
                    order=order,
                    status=Order.Status.PAYMENT_PENDING,
                    notes=f"Order created via Secure Checkout REST API ({payment_method}).",
                    changed_by=request.user if request.user.is_authenticated else None,
                )

                # Initiate Gateway Order
                rzp_service = RazorpayService()
                rzp_order = rzp_service.create_order(order)

                return Response(
                    {
                        "order_id": str(order.id),
                        "order_number": order.order_number,
                        "total_amount": str(order.total_amount),
                        "currency": rzp_service.currency,
                        "payment_method": payment_method,
                        "razorpay_order_id": rzp_order["id"],
                        "razorpay_key_id": rzp_service.key_id,
                    },
                    status=status.HTTP_201_CREATED,
                )

        except InsufficientStockError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response(
                {"error": f"Order processing failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PaymentVerifyAPIView(views.APIView):
    """
    POST /api/v1/payments/verify/
    Verifies Razorpay HMAC signature on the server.
    Updates order to PAID, finalizes stock deduction, creates Payment.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PaymentVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        order = get_object_or_404(Order, order_number=data["order_number"])

        rzp_service = RazorpayService()
        is_valid = rzp_service.verify_payment_signature(
            razorpay_order_id=data["razorpay_order_id"],
            razorpay_payment_id=data["razorpay_payment_id"],
            razorpay_signature=data["razorpay_signature"],
        )

        if not is_valid:
            AuditLog.objects.create(
                action="SECURITY_ALERT",
                resource_type="PaymentVerification",
                resource_id=order.order_number,
                details={"reason": "Invalid payment signature attempt", "data": data},
            )
            return Response(
                {"error": "Cryptographic signature verification failed. Untrusted payment payload."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            order.status = Order.Status.PAID
            order.save(update_fields=["status", "updated_at"])

            # Deduct inventory permanently
            for item in order.items.all():
                if hasattr(item.product, "inventory"):
                    item.product.inventory.commit_sale(
                        quantity=item.quantity,
                        reference_id=order.order_number,
                        user=order.user,
                    )

            Payment.objects.update_or_create(
                order=order,
                defaults={
                    "provider": Payment.Provider.RAZORPAY,
                    "transaction_id": data["razorpay_payment_id"],
                    "gateway_order_id": data["razorpay_order_id"],
                    "amount": order.total_amount,
                    "currency": "INR",
                    "status": Payment.Status.CAPTURED,
                    "raw_response": data,
                },
            )

            OrderStatusHistory.objects.create(
                order=order,
                status=Order.Status.PAID,
                notes=f"Payment verified via REST API (Ref: {data['razorpay_payment_id']}).",
                changed_by=order.user,
            )

            # Clear cart session
            cart = get_or_create_cart(request)
            cart.items.all().delete()

        return Response(
            {
                "success": True,
                "order_number": order.order_number,
                "status": order.status,
                "message": "Payment verified and order confirmed successfully.",
            },
            status=status.HTTP_200_OK,
        )


class PaymentWebhookAPIView(views.APIView):
    """
    POST /api/v1/payments/webhook/
    Idempotent, replay-protected webhook receiver for Razorpay payment captures.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        signature = request.META.get("HTTP_X_RAZORPAY_SIGNATURE", "")
        payload = request.body.decode("utf-8")

        rzp_service = RazorpayService()
        if not rzp_service.verify_webhook_signature(payload, signature):
            return Response({"error": "Invalid webhook signature."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event_data = json.loads(payload)
        except json.JSONDecodeError:
            return Response({"error": "Malformed payload."}, status=status.HTTP_400_BAD_REQUEST)

        success = rzp_service.process_webhook_event(event_data)
        return Response({"status": "acknowledged" if success else "ignored"}, status=status.HTTP_200_OK)


# ==============================================================================
# 2. SERVER-AUTHORITATIVE CART API
# ==============================================================================

class CartAPIView(views.APIView):
    """
    GET /api/v1/cart/ - Retrieve server-calculated cart with items and totals
    POST /api/v1/cart/items/ - Add item to cart with stock validation
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cart = get_or_create_cart(request)
        cart_totals = calculate_cart_totals(cart, request)

        serialized_items = []
        for item in cart_totals["items"]:
            serialized_items.append({
                "item_id": str(item.id),
                "product_id": str(item.product.id),
                "product_name": item.product.name,
                "variant_name": item.variant.name if item.variant else "",
                "unit_price": str(item.current_price),
                "quantity": item.quantity,
                "line_total": str(item.current_price * item.quantity),
                "image_url": item.product.primary_image_url,
            })

        return Response({
            "total_items": cart_totals["total_items"],
            "subtotal": str(cart_totals["subtotal"]),
            "discount_amount": str(cart_totals["discount_amount"]),
            "coupon_code": cart_totals["coupon_code"],
            "shipping_fee": str(cart_totals["shipping_fee"]),
            "tax_amount": str(cart_totals["tax_amount"]),
            "total": str(cart_totals["total"]),
            "items": serialized_items,
        })

    def post(self, request):
        serializer = CartItemInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=serializer.validated_data["product_id"], is_active=True)
        variant = None
        if serializer.validated_data.get("variant_id"):
            variant = get_object_or_404(ProductVariant, id=serializer.validated_data["variant_id"], product=product)

        quantity = serializer.validated_data["quantity"]

        # Validate stock
        if hasattr(product, "inventory"):
            avail = product.inventory.available_quantity
            if avail < quantity:
                return Response(
                    {"error": f"Cannot add {quantity} units. Only {avail} units available in stock."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        cart = get_or_create_cart(request)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={"quantity": quantity},
        )
        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity", "updated_at"])

        return Response({"success": True, "message": "Item added to cart."}, status=status.HTTP_201_CREATED)


class CartItemDeleteAPIView(views.APIView):
    """
    DELETE /api/v1/cart/items/<uuid:item_id>/
    """
    permission_classes = [permissions.AllowAny]

    def delete(self, request, item_id):
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        return Response({"success": True, "message": "Item removed from cart."}, status=status.HTTP_200_OK)


# ==============================================================================
# 3. AUTHENTICATION & USER API
# ==============================================================================

class AuthRegisterAPIView(views.APIView):
    """
    POST /api/v1/auth/register/
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(UserProfileSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthLoginAPIView(views.APIView):
    """
    POST /api/v1/auth/login/
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            return Response(UserProfileSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthLogoutAPIView(views.APIView):
    """
    POST /api/v1/auth/logout/
    """
    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


class AuthProfileAPIView(views.APIView):
    """
    GET /api/v1/auth/profile/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserProfileSerializer(request.user).data)


# ==============================================================================
# 4. PROTECTED ADMINISTRATIVE & RBAC API
# ==============================================================================

class AdminProductListCreateAPIView(views.APIView):
    """
    GET, POST /api/v1/admin/products/
    Strictly protected: only Staff/Managers can query or create products.
    """
    permission_classes = [IsStaffOrManager]

    def get(self, request):
        products = Product.objects.all().select_related("category").prefetch_related("images", "variants")[:50]
        return Response(ProductSerializer(products, many=True).data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminInventoryAdjustAPIView(views.APIView):
    """
    POST /api/v1/admin/inventory/adjust/
    Enforces atomic stock adjustments and records stock movement ledger.
    """
    permission_classes = [IsStaffOrManager]

    def post(self, request):
        serializer = InventoryAdjustSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        sku = serializer.validated_data["sku"]
        change = serializer.validated_data["quantity_change"]
        mtype = serializer.validated_data["movement_type"]
        notes = serializer.validated_data.get("notes", "")

        inv = get_object_or_404(InventoryItem, sku=sku)

        with transaction.atomic():
            new_qty = inv.quantity_on_hand + change
            if new_qty < 0:
                return Response(
                    {"error": f"Adjustment would result in negative inventory ({new_qty})."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            inv.quantity_on_hand = new_qty
            inv.save(update_fields=["quantity_on_hand", "updated_at"])

            StockMovement.objects.create(
                inventory_item=inv,
                movement_type=mtype,
                quantity=change,
                reference_id="API_ADJUST",
                notes=notes,
                user=request.user,
            )

        return Response(
            {
                "success": True,
                "sku": inv.sku,
                "new_quantity_on_hand": inv.quantity_on_hand,
                "available_quantity": inv.available_quantity,
            },
            status=status.HTTP_200_OK,
        )


class AdminOrderListAPIView(views.APIView):
    """
    GET /api/v1/admin/orders/
    """
    permission_classes = [IsStaffOrManager]

    def get(self, request):
        orders = Order.objects.all().order_by("-created_at")[:50]
        return Response(OrderDetailSerializer(orders, many=True).data)


class AdminOrderStatusUpdateAPIView(views.APIView):
    """
    PATCH /api/v1/admin/orders/<uuid:order_id>/status/
    """
    permission_classes = [IsStaffOrManager]

    def patch(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderStatusUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_status = serializer.validated_data["status"]
        old_status = order.status
        order.status = new_status
        if serializer.validated_data.get("tracking_number"):
            order.tracking_number = serializer.validated_data["tracking_number"]
        order.save()

        OrderStatusHistory.objects.create(
            order=order,
            status=new_status,
            notes=serializer.validated_data.get("notes", f"Status updated to {new_status} via Admin API."),
            changed_by=request.user,
        )

        return Response({"success": True, "order_number": order.order_number, "status": order.status})


# ==============================================================================
# 5. CUSTOMER ORDER HISTORY & LIVE TRACKING API
# ==============================================================================

class CustomerOrderListAPIView(views.APIView):
    """
    GET /api/v1/orders/
    Returns orders placed by the currently authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = CustomerOrderListSerializer(orders, many=True)
        return Response({
            "success": True,
            "count": orders.count(),
            "results": serializer.data,
        })


class CustomerOrderDetailAPIView(views.APIView):
    """
    GET /api/v1/orders/<str:order_number>/
    Returns full order details, line items, and audit history.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_number):
        if request.user.is_staff or getattr(request.user, "is_manager", False):
            order = get_object_or_404(Order, order_number=order_number)
        else:
            order = get_object_or_404(Order, order_number=order_number, user=request.user)
        serializer = CustomerOrderDetailSerializer(order)
        return Response({
            "success": True,
            "order": serializer.data,
        })


class OrderLiveTrackingAPIView(views.APIView):
    """
    GET /api/v1/orders/track/<str:order_number>/
    Public live order fulfillment and shipment tracking timeline.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number)
        shipment = getattr(order, "shipment", None)

        timeline = order.status_history.all().order_by("created_at")
        timeline_data = [
            {
                "id": str(item.id),
                "status": item.status,
                "notes": item.notes,
                "created_at": item.created_at,
            }
            for item in timeline
        ]

        tracking_data = {
            "order_number": order.order_number,
            "status": order.status,
            "carrier": order.carrier or (shipment.carrier if shipment else ""),
            "tracking_number": order.tracking_number or (shipment.tracking_number if shipment else ""),
            "shipped_at": shipment.shipped_at if shipment else None,
            "estimated_delivery": shipment.estimated_delivery if shipment else None,
            "is_delivered": order.status == Order.Status.DELIVERED,
            "timeline": timeline_data,
        }
        serializer = OrderLiveTrackingSerializer(tracking_data)
        return Response({
            "success": True,
            "tracking": serializer.data,
        })


class OrderShippingAddressUpdateAPIView(views.APIView):
    """
    PATCH /api/v1/orders/<str:order_number>/shipping-address/
    Allows customer to update shipping address before order is dispatched.
    Rejects update if already in SHIPPED or DELIVERED status.
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, order_number):
        if request.user.is_staff or getattr(request.user, "is_manager", False):
            order = get_object_or_404(Order, order_number=order_number)
        else:
            order = get_object_or_404(Order, order_number=order_number, user=request.user)

        # Invariant: Shipping address cannot be mutated once fulfillment has dispatched
        disallowed_statuses = [Order.Status.SHIPPED, Order.Status.DELIVERED, Order.Status.CANCELLED, Order.Status.REFUNDED]
        if order.status in disallowed_statuses:
            return Response(
                {
                    "error": f"Shipping address cannot be modified. Order is currently in '{order.status}' status.",
                    "order_status": order.status,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = OrderShippingAddressUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        for field, value in data.items():
            if hasattr(order, field) and value is not None:
                setattr(order, field, value)

        order.save()

        OrderStatusHistory.objects.create(
            order=order,
            status=order.status,
            notes=f"Shipping address updated by customer: {order.shipping_city}, {order.shipping_postal_code}",
            changed_by=request.user,
        )

        return Response({
            "success": True,
            "message": "Shipping address updated successfully.",
            "order_number": order.order_number,
            "updated_address": {
                "shipping_full_name": order.shipping_full_name,
                "shipping_phone": order.shipping_phone,
                "shipping_address_line_1": order.shipping_address_line_1,
                "shipping_address_line_2": order.shipping_address_line_2,
                "shipping_city": order.shipping_city,
                "shipping_state": order.shipping_state,
                "shipping_postal_code": order.shipping_postal_code,
            },
        })


# ==============================================================================
# 6. EXTERNAL ERP & LOGISTICS WEBHOOK API
# ==============================================================================

class ErpBulkInventorySyncAPIView(views.APIView):
    """
    POST /api/v1/erp/inventory/bulk-sync/
    External ERP system inventory synchronization.
    Atomically updates warehouse on-hand stock and logs stock movements.
    """
    permission_classes = [IsStaffOrManager]

    def post(self, request):
        serializer = ErpBulkInventorySyncSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        batch_id = serializer.validated_data["batch_id"]
        items_payload = serializer.validated_data["items"]
        updated_records = []
        errors = []

        with transaction.atomic():
            for item_data in items_payload:
                sku = item_data["sku"]
                new_qoh = item_data["quantity_on_hand"]
                try:
                    inv_item = InventoryItem.objects.select_for_update().get(sku=sku)
                    diff = new_qoh - inv_item.quantity_on_hand
                    inv_item.quantity_on_hand = new_qoh
                    inv_item.save(update_fields=["quantity_on_hand", "updated_at"])

                    movement_type = (
                        StockMovement.MovementType.PURCHASE_RECEIPT
                        if diff >= 0
                        else StockMovement.MovementType.ADJUSTMENT_MANUAL
                    )
                    StockMovement.objects.create(
                        inventory_item=inv_item,
                        movement_type=movement_type,
                        quantity=diff,
                        reference_id=f"ERP-{batch_id}",
                        notes=f"ERP inventory sync batch {batch_id}",
                        user=request.user if request.user.is_authenticated else None,
                    )
                    updated_records.append({
                        "sku": sku,
                        "new_quantity_on_hand": new_qoh,
                        "available_quantity": inv_item.available_quantity,
                    })
                except InventoryItem.DoesNotExist:
                    errors.append({"sku": sku, "error": "SKU not found in catalog."})

        return Response({
            "success": True,
            "batch_id": batch_id,
            "processed_count": len(updated_records),
            "updated": updated_records,
            "unmatched_skus": errors,
        }, status=status.HTTP_200_OK)


class LogisticsDispatchAPIView(views.APIView):
    """
    POST /api/v1/erp/logistics/dispatch/
    Third-party logistics (3PL) dispatch webhook.
    Transitions order to SHIPPED and registers tracking metadata.
    """
    permission_classes = [IsStaffOrManager]

    def post(self, request):
        serializer = LogisticsDispatchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order_number = serializer.validated_data["order_number"]
        carrier = serializer.validated_data["carrier"]
        tracking_number = serializer.validated_data["tracking_number"]
        est_delivery = serializer.validated_data.get("estimated_delivery")
        notes = serializer.validated_data.get("dispatch_notes", f"Dispatched via {carrier}")

        order = get_object_or_404(Order, order_number=order_number)
        order.status = Order.Status.SHIPPED
        order.carrier = carrier
        order.tracking_number = tracking_number
        order.save(update_fields=["status", "carrier", "tracking_number", "updated_at"])

        # Create or update Shipment model
        Shipment.objects.update_or_create(
            order=order,
            defaults={
                "carrier": carrier,
                "tracking_number": tracking_number,
                "estimated_delivery": est_delivery,
            },
        )

        OrderStatusHistory.objects.create(
            order=order,
            status=Order.Status.SHIPPED,
            notes=f"Dispatched by logistics carrier {carrier}. AWB/Tracking #{tracking_number}. {notes}",
            changed_by=request.user if request.user.is_authenticated else None,
        )

        return Response({
            "success": True,
            "order_number": order.order_number,
            "status": order.status,
            "carrier": carrier,
            "tracking_number": tracking_number,
            "tracking_url": f"/api/v1/orders/track/{order.order_number}/",
        }, status=status.HTTP_200_OK)


class ErpGenericWebhookListenerAPIView(views.APIView):
    """
    POST /api/v1/erp/webhooks/listener/
    External event listener with audit logging.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ErpGenericWebhookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        event_type = serializer.validated_data["event_type"]
        event_id = serializer.validated_data.get("event_id", "")
        payload = serializer.validated_data["data"]

        AuditLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            user_email=request.user.email if request.user.is_authenticated else "",
            action="SECURITY_EVENT",
            resource_type="ExternalWebhook",
            resource_id=event_id or "EVENT",
            details={
                "event_type": event_type,
                "event_id": event_id,
                "payload_keys": list(payload.keys()),
            },
            ip_address=request.META.get("REMOTE_ADDR"),
        )

        return Response({
            "success": True,
            "received_event": event_type,
            "event_id": event_id,
            "status": "acknowledged",
        }, status=status.HTTP_200_OK)
