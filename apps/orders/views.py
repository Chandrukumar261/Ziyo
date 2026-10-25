from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, OrderStatusHistory, ReturnRequest
from .forms import CheckoutForm, ReturnRequestForm
from apps.cart.cart_service import get_or_create_cart, calculate_cart_totals
from apps.inventory.models import InsufficientStockError
from apps.accounts.models import CustomerAddress
from apps.core.countries import get_country_name
from apps.payments.razorpay_service import RazorpayService

def checkout_view(request):
    """
    Validates cart, calculates server totals, reserves stock, creates pending Order transactionally.
    Supports Credit/Debit Cards, Razorpay UPI/NetBanking, and Cash on Delivery (COD).
    """
    cart = get_or_create_cart(request)
    cart_totals = calculate_cart_totals(cart, request)

    if cart_totals["total_items"] == 0:
        messages.warning(request, "Your cart is empty. Please add items before checking out.")
        return redirect("cart:cart_detail")

    # Initial form data populated from user profile / default address if logged in
    initial_data = {"country": "IN", "payment_method": "RAZORPAY_CARD"}
    saved_addresses = []
    if request.user.is_authenticated:
        initial_data["email"] = request.user.email
        initial_data["phone"] = request.user.phone
        initial_data["full_name"] = request.user.full_name
        saved_addresses = request.user.addresses.all()
        default_addr = saved_addresses.filter(is_default=True).first() or saved_addresses.first()
        if default_addr:
            initial_data["address_line_1"] = default_addr.address_line_1
            initial_data["address_line_2"] = default_addr.address_line_2
            initial_data["city"] = default_addr.city
            initial_data["state"] = default_addr.state
            initial_data["postal_code"] = default_addr.postal_code
            if hasattr(default_addr, "country") and default_addr.country:
                initial_data["country"] = default_addr.country

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                chosen_method = form.cleaned_data.get("payment_method", "RAZORPAY_CARD")
                country_code = form.cleaned_data.get("country", "IN")
                country_name = get_country_name(country_code)

                with transaction.atomic():
                    # Recheck product stock before committing
                    for item in cart_totals["items"]:
                        if hasattr(item.product, "inventory"):
                            avail = item.product.inventory.available_quantity
                            if avail < item.quantity:
                                raise InsufficientStockError(
                                    f"Sorry, {item.product.name} only has {avail} items left in stock."
                                )

                    # Create authoritative order
                    order = Order.objects.create(
                        order_number=Order.generate_order_number(),
                        user=request.user if request.user.is_authenticated else None,
                        email=form.cleaned_data["email"],
                        phone=form.cleaned_data["phone"],
                        status=Order.Status.PROCESSING if chosen_method == "COD" else Order.Status.PAYMENT_PENDING,
                        subtotal=cart_totals["subtotal"],
                        discount_amount=cart_totals["discount_amount"],
                        coupon_code=cart_totals["coupon_code"],
                        shipping_fee=cart_totals["shipping_fee"],
                        tax_amount=cart_totals["tax_amount"],
                        total_amount=cart_totals["total"],
                        shipping_full_name=form.cleaned_data["full_name"],
                        shipping_phone=form.cleaned_data["phone"],
                        shipping_address_line_1=form.cleaned_data["address_line_1"],
                        shipping_address_line_2=form.cleaned_data["address_line_2"],
                        shipping_city=form.cleaned_data["city"],
                        shipping_state=form.cleaned_data["state"],
                        shipping_postal_code=form.cleaned_data["postal_code"],
                        shipping_country=country_name,
                        customer_notes=form.cleaned_data["customer_notes"],
                    )

                    # Create line item snapshots and hold inventory
                    for item in cart_totals["items"]:
                        unit_p = item.current_price
                        line_tot = unit_p * item.quantity
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            product_name=item.product.name,
                            variant_name=item.variant.name if item.variant else "",
                            sku=item.variant.sku if item.variant else item.product.sku,
                            unit_price=unit_p,
                            quantity=item.quantity,
                            line_total=line_tot,
                        )

                        # Hold/reserve stock
                        if hasattr(item.product, "inventory"):
                            item.product.inventory.reserve_stock(
                                quantity=item.quantity,
                                reference_id=order.order_number,
                            )

                    # Handle payment workflow branch
                    if chosen_method == "COD":
                        RazorpayService.finalize_cod_order(order)
                        # Clear customer shopping cart
                        cart.items.all().delete()
                        if "coupon_code" in request.session:
                            del request.session["coupon_code"]
                        messages.success(
                            request,
                            f"Order #{order.order_number} confirmed with Cash on Delivery! Please keep ₹{order.total_amount} ready upon delivery."
                        )
                        return redirect("orders:order_success", order_number=order.order_number)
                    else:
                        # Initial status history for online payment
                        OrderStatusHistory.objects.create(
                            order=order,
                            status=Order.Status.PAYMENT_PENDING,
                            notes=f"Order created, proceeding to Razorpay gateway ({chosen_method}).",
                            changed_by=request.user if request.user.is_authenticated else None,
                        )

                # Redirect to payment gateway with preferred method parameter
                redirect_url = f"{reverse('payments:initiate_payment', kwargs={'order_number': order.order_number})}?method={chosen_method}"
                return redirect(redirect_url)

            except InsufficientStockError as exc:
                messages.error(request, str(exc))
                return redirect("cart:cart_detail")
    else:
        form = CheckoutForm(initial=initial_data)

    context = {
        "form": form,
        "saved_addresses": saved_addresses,
        **cart_totals,
    }
    return render(request, "checkout/checkout.html", context)


@login_required
def order_list_view(request):
    """Authenticated customer's order history."""
    orders = request.user.orders.all().prefetch_related("items").order_by("-created_at")
    return render(request, "orders/order_list.html", {"orders": orders})


def order_detail_view(request, order_number):
    """View details of an order."""
    order = get_object_or_404(Order.objects.prefetch_related("items", "status_history"), order_number=order_number)

    # Permission check: If user authenticated, must own the order or be staff
    if request.user.is_authenticated:
        if order.user and order.user != request.user and not request.user.is_staff:
            messages.error(request, "You do not have permission to view this order.")
            return redirect("catalog:home")

    return render(request, "orders/order_detail.html", {"order": order})


def order_success_view(request, order_number):
    """Order confirmation receipt."""
    order = get_object_or_404(Order.objects.prefetch_related("items"), order_number=order_number)
    return render(request, "orders/order_success.html", {"order": order})


@login_required
def return_request_view(request, order_number):
    """Customer initiates a return/refund request for delivered order."""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    if request.method == "POST":
        form = ReturnRequestForm(request.POST)
        if form.is_valid():
            ret = form.save(commit=False)
            ret.order = order
            ret.user = request.user
            ret.save()
            messages.success(request, "Your return request has been submitted for review.")
            return redirect("orders:order_detail", order_number=order.order_number)
    else:
        form = ReturnRequestForm()

    return render(request, "orders/return_request.html", {"order": order, "form": form})
