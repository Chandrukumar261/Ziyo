import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.catalog.models import Product, ProductVariant

class Cart(TimeStampedModel):
    """
    Shopping cart instance tied to authenticated customer or anonymous session key.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts",
        null=True,
        blank=True,
    )
    session_key = models.CharField(max_length=80, null=True, blank=True, db_index=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        owner = self.user.email if self.user else f"Guest ({self.session_key})"
        return f"Cart {self.id} for {owner}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        """Calculates current subtotal using current live product prices."""
        total = Decimal("0.00")
        for item in self.items.select_related("product", "variant"):
            total += item.current_price * item.quantity
        return total.quantize(Decimal("0.01"))


class CartItem(TimeStampedModel):
    """Line item in a shopping cart."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["created_at"]
        unique_together = ("cart", "product", "variant")

    def __str__(self):
        variant_str = f" - {self.variant.name}" if self.variant else ""
        return f"{self.quantity}x {self.product.name}{variant_str}"

    @property
    def current_price(self):
        """Always returns the live authoritative price from database."""
        if self.variant and self.variant.price_override is not None:
            return self.variant.price_override
        return self.product.price

    @property
    def line_total(self):
        return (self.current_price * self.quantity).quantize(Decimal("0.01"))


class Wishlist(TimeStampedModel):
    """Customer wishlist."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist",
    )

    def __str__(self):
        return f"Wishlist of {self.user.email}"


class WishlistItem(TimeStampedModel):
    """Item in customer's wishlist."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_items")

    class Meta:
        unique_together = ("wishlist", "product")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.name} in wishlist"
