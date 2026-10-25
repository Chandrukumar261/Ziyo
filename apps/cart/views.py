from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CartItem, Wishlist, WishlistItem
from .cart_service import get_or_create_cart, calculate_cart_totals
from apps.catalog.models import Product, ProductVariant

def cart_detail_view(request):
    """Customer shopping cart view with calculated totals, taxes, shipping, and coupon."""
    cart = get_or_create_cart(request)
    cart_data = calculate_cart_totals(cart, request)
    return render(request, "cart/cart.html", cart_data)


@require_POST
def add_to_cart_view(request, product_id):
    """Adds a product or variant to cart."""
    product = get_object_or_404(Product, id=product_id, is_active=True, is_archived=False)
    cart = get_or_create_cart(request)

    variant_id = request.POST.get("variant_id")
    quantity_raw = request.POST.get("quantity", "1")
    try:
        quantity = max(1, int(quantity_raw))
    except (ValueError, TypeError):
        quantity = 1

    variant = None
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product, is_active=True)

    # Check stock limit if inventory item exists
    if hasattr(product, "inventory"):
        avail = product.inventory.available_quantity
        if avail < quantity:
            messages.error(request, f"Sorry, only {avail} units available for {product.name}.")
            return redirect("catalog:product_detail", slug=product.slug)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        variant=variant,
        defaults={"quantity": quantity},
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    messages.success(request, f"Added {product.name} to your cart.")
    return redirect("cart:cart_detail")


@require_POST
def update_cart_quantity_view(request, item_id):
    """Update item quantity or remove if quantity is 0."""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    quantity_raw = request.POST.get("quantity", "1")
    try:
        quantity = int(quantity_raw)
    except (ValueError, TypeError):
        quantity = 1

    if quantity <= 0:
        cart_item.delete()
        messages.info(request, "Item removed from cart.")
    else:
        # Check stock constraint
        if hasattr(cart_item.product, "inventory"):
            avail = cart_item.product.inventory.available_quantity
            if quantity > avail:
                quantity = avail
                messages.warning(request, f"Quantity adjusted to available stock ({avail}).")
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated.")

    return redirect("cart:cart_detail")


@require_POST
def remove_from_cart_view(request, item_id):
    """Remove line item from shopping cart."""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    messages.info(request, f"Removed {cart_item.product.name} from your cart.")
    return redirect("cart:cart_detail")


@login_required
def wishlist_view(request):
    """Customer wishlist view."""
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.items.select_related("product").prefetch_related("product__images")
    return render(request, "cart/wishlist.html", {"items": items})


@login_required
@require_POST
def toggle_wishlist_view(request, product_id):
    """Toggles a product in customer's wishlist."""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    item = WishlistItem.objects.filter(wishlist=wishlist, product=product).first()

    if item:
        item.delete()
        messages.info(request, f"Removed {product.name} from your wishlist.")
    else:
        WishlistItem.objects.create(wishlist=wishlist, product=product)
        messages.success(request, f"Saved {product.name} to your wishlist!")

    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "cart:wishlist"
    return redirect(next_url)
