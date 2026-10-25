import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import Payment, PaymentAttempt, PaymentWebhookEvent
from .razorpay_service import RazorpayService
from apps.orders.models import Order
from apps.cart.cart_service import get_or_create_cart
from apps.core.models import AuditLog

def initiate_payment_view(request, order_number):
    """
    Renders the secure checkout payment gateway page with Razorpay integration.
    """
    order = get_object_or_404(Order, order_number=order_number)

    # Security check: If authenticated customer, ensure order belongs to them
    if request.user.is_authenticated and order.user and order.user != request.user:
        messages.error(request, "Unauthorized access to order.")
        return redirect("catalog:home")

    if order.status == Order.Status.PAID:
        return redirect("orders:order_success", order_number=order.order_number)

    service = RazorpayService()
    gateway_order = service.create_order(order)

    # Record PaymentAttempt
    PaymentAttempt.objects.create(
        order=order,
        gateway_order_id=gateway_order["id"],
        status="INITIATED",
    )

    selected_method = request.GET.get("method", "RAZORPAY_CARD")

    context = {
        "order": order,
        "selected_method": selected_method,
        "razorpay_key_id": service.key_id,
        "gateway_order_id": gateway_order["id"],
        "amount_paise": gateway_order["amount"],
        "currency": service.currency,
    }
    return render(request, "checkout/payment_gateway.html", context)


@require_POST
def switch_to_cod_view(request, order_number):
    """Allows customer on payment page to choose Cash on Delivery instead."""
    order = get_object_or_404(Order, order_number=order_number)
    if request.user.is_authenticated and order.user and order.user != request.user:
        messages.error(request, "Unauthorized access to order.")
        return redirect("catalog:home")

    if order.status in [Order.Status.PAID, Order.Status.CANCELLED]:
        messages.warning(request, f"Cannot switch payment method for order in {order.status} status.")
        return redirect("orders:order_detail", order_number=order.order_number)

    RazorpayService.finalize_cod_order(order)
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    if "coupon_code" in request.session:
        del request.session["coupon_code"]

    messages.success(request, f"Order #{order.order_number} confirmed with Cash on Delivery! Please keep ₹{order.total_amount} ready upon delivery.")
    return redirect("orders:order_success", order_number=order.order_number)


@require_POST
def payment_callback_view(request):
    """
    Verifies the server-side HMAC signature returned by Razorpay client checkout.
    """
    razorpay_order_id = request.POST.get("razorpay_order_id", "").strip()
    razorpay_payment_id = request.POST.get("razorpay_payment_id", "").strip()
    razorpay_signature = request.POST.get("razorpay_signature", "").strip()
    order_number = request.POST.get("order_number", "").strip()

    order = get_object_or_404(Order, order_number=order_number)
    service = RazorpayService()

    is_valid = service.verify_payment_signature(
        razorpay_order_id=razorpay_order_id,
        razorpay_payment_id=razorpay_payment_id,
        razorpay_signature=razorpay_signature,
    )

    if not is_valid:
        AuditLog.objects.create(
            user=order.user,
            user_email=order.email,
            action="PAYMENT_FAILED",
            resource_type="Order",
            resource_id=order.order_number,
            details={
                "reason": "Invalid payment signature attempt",
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
            },
        )
        messages.error(request, "Payment verification failed: Invalid cryptographic signature.")
        return redirect("payments:payment_failure", order_number=order.order_number)

    # Finalize payment & order
    service.finalize_paid_order(
        order=order,
        payment_id=razorpay_payment_id,
        gateway_order_id=razorpay_order_id,
        payment_method="RAZORPAY_ONLINE",
        raw_data={"signature": razorpay_signature},
    )

    # Clear shopping cart after successful purchase
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    if "coupon_code" in request.session:
        del request.session["coupon_code"]

    messages.success(request, f"Payment successful! Order #{order.order_number} is confirmed.")
    return redirect("orders:order_success", order_number=order.order_number)


def payment_failure_view(request, order_number):
    """Payment failure notification page."""
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, "checkout/payment_failure.html", {"order": order})


@csrf_exempt
@require_POST
def razorpay_webhook_view(request):
    """
    Webhook handler for asynchronous status updates with duplicate webhook protection.
    """
    signature = request.META.get("HTTP_X_RAZORPAY_SIGNATURE", "")
    body_bytes = request.body
    service = RazorpayService()

    if not service.verify_webhook_signature(body_bytes, signature):
        return HttpResponse("Invalid Webhook Signature", status=400)

    try:
        data = json.loads(body_bytes.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON", status=400)

    event_id = data.get("event_id") or data.get("id") or str(timezone.now().timestamp())
    event_type = data.get("event", "")

    # Duplicate webhook protection
    existing = PaymentWebhookEvent.objects.filter(event_id=event_id).first()
    if existing and existing.is_processed:
        return HttpResponse("Event Already Processed", status=200)

    webhook_record, _ = PaymentWebhookEvent.objects.get_or_create(
        event_id=event_id,
        defaults={
            "event_type": event_type,
            "provider": "RAZORPAY",
            "payload": data,
        },
    )

    if event_type == "payment.captured":
        payment_entity = data.get("payload", {}).get("payment", {}).get("entity", {})
        gateway_order_id = payment_entity.get("order_id")
        payment_id = payment_entity.get("id")
        notes = payment_entity.get("notes", {})
        order_number = notes.get("order_number")

        order = None
        if order_number:
            order = Order.objects.filter(order_number=order_number).first()
        elif gateway_order_id:
            attempt = PaymentAttempt.objects.filter(gateway_order_id=gateway_order_id).first()
            if attempt:
                order = attempt.order

        if order:
            service.finalize_paid_order(
                order=order,
                payment_id=payment_id,
                gateway_order_id=gateway_order_id,
                payment_method=payment_entity.get("method", "WEBHOOK"),
                raw_data=payment_entity,
            )

    webhook_record.is_processed = True
    webhook_record.processed_at = timezone.now()
    webhook_record.save()

    return JsonResponse({"status": "acknowledged"})
