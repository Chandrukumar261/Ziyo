from .cart_service import get_or_create_cart

def cart_summary(request):
    """Provides current cart item count to global storefront navigation."""
    try:
        cart = get_or_create_cart(request)
        count = cart.total_items
        subtotal = cart.subtotal
    except Exception:
        count = 0
        subtotal = 0
    return {
        "cart_item_count": count,
        "cart_subtotal": subtotal,
    }
