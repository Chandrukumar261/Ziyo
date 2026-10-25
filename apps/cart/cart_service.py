from decimal import Decimal
from django.utils import timezone
from .models import Cart, CartItem
from apps.discounts.models import Coupon

# Pricing rules
FREE_SHIPPING_THRESHOLD = Decimal("1499.00")
STANDARD_SHIPPING_FEE = Decimal("99.00")
TAX_PERCENTAGE = Decimal("5.00")  # 5% GST

def get_or_create_cart(request):
    """
    Returns the user's Cart. Migrates anonymous session cart items to user's cart on login.
    """
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key

    if request.user.is_authenticated:
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        # Check if an anonymous cart exists with session_key
        if session_key:
            guest_carts = Cart.objects.filter(session_key=session_key, user__isnull=True)
            for guest_cart in guest_carts:
                for item in guest_cart.items.all():
                    existing_item = user_cart.items.filter(
                        product=item.product,
                        variant=item.variant,
                    ).first()
                    if existing_item:
                        existing_item.quantity += item.quantity
                        existing_item.save()
                    else:
                        item.cart = user_cart
                        item.save()
                guest_cart.delete()
        return user_cart
    else:
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user__isnull=True)
        return cart


def calculate_cart_totals(cart, request):
    """
    Authoritative server-side calculation of subtotal, discounts, shipping, tax, and final order total.
    """
    subtotal = cart.subtotal
    total_items = cart.total_items

    # Shipping Calculation
    if subtotal == 0:
        shipping_fee = Decimal("0.00")
    elif subtotal >= FREE_SHIPPING_THRESHOLD:
        shipping_fee = Decimal("0.00")
    else:
        shipping_fee = STANDARD_SHIPPING_FEE

    # Coupon validation & calculation
    coupon_code = request.session.get("coupon_code", "")
    coupon = None
    discount_amount = Decimal("0.00")
    coupon_message = ""

    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            is_valid, reason = coupon.is_valid(
                user=request.user if request.user.is_authenticated else None,
                subtotal=subtotal,
            )
            if is_valid:
                discount_amount = coupon.calculate_discount(subtotal=subtotal, shipping_fee=shipping_fee)
            else:
                coupon_message = reason
                if "coupon_code" in request.session:
                    del request.session["coupon_code"]
                coupon = None
        except Coupon.DoesNotExist:
            if "coupon_code" in request.session:
                del request.session["coupon_code"]

    # Tax Calculation (applied on discounted subtotal)
    taxable_amount = max(Decimal("0.00"), subtotal - discount_amount)
    tax_amount = ((taxable_amount * TAX_PERCENTAGE) / Decimal("100.00")).quantize(Decimal("0.01"))

    # Final Total
    total = (taxable_amount + shipping_fee + tax_amount).quantize(Decimal("0.01"))

    return {
        "cart": cart,
        "items": cart.items.select_related("product", "variant").prefetch_related("product__images"),
        "total_items": total_items,
        "subtotal": subtotal,
        "shipping_fee": shipping_fee,
        "free_shipping_threshold": FREE_SHIPPING_THRESHOLD,
        "free_shipping_needed": max(Decimal("0.00"), FREE_SHIPPING_THRESHOLD - subtotal),
        "coupon": coupon,
        "coupon_code": coupon_code if coupon else "",
        "discount_amount": discount_amount,
        "coupon_message": coupon_message,
        "tax_amount": tax_amount,
        "tax_percentage": TAX_PERCENTAGE,
        "total": total,
    }
