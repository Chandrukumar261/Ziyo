import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.core.models import TimeStampedModel

class Coupon(TimeStampedModel):
    """Promotional coupon codes with multi-rule server-side validation."""

    class DiscountType(models.TextChoices):
        PERCENTAGE = "PERCENTAGE", "Percentage Discount (%)"
        FIXED_AMOUNT = "FIXED_AMOUNT", "Fixed Amount"
        FREE_SHIPPING = "FREE_SHIPPING", "Free Shipping"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=30, unique=True, db_index=True)
    discount_type = models.CharField(
        max_length=20,
        choices=DiscountType.choices,
        default=DiscountType.PERCENTAGE,
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Percentage (e.g. 15 for 15%) or fixed amount (e.g. 200.00)"
    )
    min_purchase_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Minimum subtotal required to use coupon"
    )
    max_discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Capped maximum discount value for percentage coupons"
    )
    usage_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum total times this coupon can be redeemed across all users"
    )
    per_user_limit = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return f"{self.code} ({self.discount_type}: {self.value})"

    def clean(self):
        self.code = self.code.upper().strip()
        if self.valid_to and self.valid_from and self.valid_to <= self.valid_from:
            raise ValidationError("Coupon expiration date must be after start date.")

    def save(self, *args, **kwargs):
        self.code = self.code.upper().strip()
        super().save(*args, **kwargs)

    def is_valid(self, user=None, subtotal=Decimal("0.00")):
        """
        Server-side validation of active status, date range, limits, and order subtotal.
        Returns (is_valid: bool, reason: str)
        """
        now = timezone.now()
        if not self.is_active:
            return False, "This coupon is no longer active."
        if now < self.valid_from or now > self.valid_to:
            return False, "This coupon has expired or is not yet valid."
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False, "This coupon has reached its total usage limit."
        if subtotal < self.min_purchase_amount:
            return False, f"Minimum purchase amount of ₹{self.min_purchase_amount} required."

        if user and user.is_authenticated:
            user_redemptions = self.redemptions.filter(user=user).count()
            if user_redemptions >= self.per_user_limit:
                return False, "You have already used this coupon the maximum allowed times."

        return True, "Coupon applied successfully!"

    def calculate_discount(self, subtotal=Decimal("0.00"), shipping_fee=Decimal("0.00")):
        """Calculates discount amount safely with Decimal precision."""
        if self.discount_type == self.DiscountType.PERCENTAGE:
            discount = (subtotal * self.value) / Decimal("100.00")
            if self.max_discount_amount and discount > self.max_discount_amount:
                discount = self.max_discount_amount
            return min(discount, subtotal).quantize(Decimal("0.01"))
        elif self.discount_type == self.DiscountType.FIXED_AMOUNT:
            return min(self.value, subtotal).quantize(Decimal("0.01"))
        elif self.discount_type == self.DiscountType.FREE_SHIPPING:
            return shipping_fee.quantize(Decimal("0.01"))
        return Decimal("0.00")


class CouponRedemption(TimeStampedModel):
    """Tracks each applied coupon for an order to prevent double usage."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="redemptions")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="coupon_redemptions",
        null=True,
        blank=True,
    )
    order_id = models.CharField(max_length=120, db_index=True)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Coupon Redemption"
        verbose_name_plural = "Coupon Redemptions"

    def __str__(self):
        return f"{self.coupon.code} on Order {self.order_id}: ₹{self.discount_amount}"
