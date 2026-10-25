import uuid
from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.core.models import TimeStampedModel
from apps.catalog.models import Product, ProductVariant

class InsufficientStockError(Exception):
    """Raised when an inventory operation exceeds available stock."""
    pass


class InventoryItem(TimeStampedModel):
    """Tracks stock on hand, reserved stock, and threshold levels."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory",
        null=True,
        blank=True,
    )
    variant = models.OneToOneField(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="inventory",
        null=True,
        blank=True,
    )
    sku = models.CharField(max_length=80, unique=True, db_index=True)
    quantity_on_hand = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)

    class Meta:
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory Items"

    def __str__(self):
        item_name = self.variant.name if self.variant else (self.product.name if self.product else "Unknown")
        return f"{item_name} [{self.sku}] - Available: {self.available_quantity}"

    @property
    def available_quantity(self):
        """Calculates instantly purchasable inventory."""
        return max(0, self.quantity_on_hand - self.reserved_quantity)

    @property
    def is_low_stock(self):
        return self.available_quantity <= self.low_stock_threshold

    @transaction.atomic
    def reserve_stock(self, quantity, reference_id=""):
        """
        Safely reserves inventory with row locking to eliminate race conditions.
        """
        item = InventoryItem.objects.select_for_update().get(pk=self.pk)
        if item.available_quantity < quantity:
            raise InsufficientStockError(
                f"Insufficient stock for {item.sku}. Available: {item.available_quantity}, Requested: {quantity}"
            )
        item.reserved_quantity += quantity
        item.save()

        StockReservation.objects.create(
            inventory_item=item,
            quantity=quantity,
            reference_id=str(reference_id),
        )
        return True

    @transaction.atomic
    def release_stock(self, quantity, reference_id=""):
        """Releases previously held stock back to available pool."""
        item = InventoryItem.objects.select_for_update().get(pk=self.pk)
        item.reserved_quantity = max(0, item.reserved_quantity - quantity)
        item.save()

        StockReservation.objects.filter(
            inventory_item=item,
            reference_id=str(reference_id),
            is_released=False,
        ).update(is_released=True)
        return True

    @transaction.atomic
    def commit_sale(self, quantity, reference_id="", user=None):
        """
        Deducts sold units from inventory on hand and decreases reserved quantity.
        """
        item = InventoryItem.objects.select_for_update().get(pk=self.pk)
        item.quantity_on_hand = max(0, item.quantity_on_hand - quantity)
        item.reserved_quantity = max(0, item.reserved_quantity - quantity)
        item.save()

        StockMovement.objects.create(
            inventory_item=item,
            movement_type=StockMovement.MovementType.ORDER_SALE,
            quantity=-quantity,
            reference_id=str(reference_id),
            notes=f"Sold via Order {reference_id}",
            user=user,
        )
        return True

    @transaction.atomic
    def adjust_stock(self, quantity_delta, reason, user=None):
        """Manual adjustment for receipts, audits, or damage."""
        item = InventoryItem.objects.select_for_update().get(pk=self.pk)
        new_quantity = item.quantity_on_hand + quantity_delta
        if new_quantity < 0:
            raise ValidationError("Quantity on hand cannot drop below zero.")
        item.quantity_on_hand = new_quantity
        item.save()

        m_type = StockMovement.MovementType.PURCHASE_RECEIPT if quantity_delta > 0 else StockMovement.MovementType.ADJUSTMENT_MANUAL
        StockMovement.objects.create(
            inventory_item=item,
            movement_type=m_type,
            quantity=quantity_delta,
            reference_id="MANUAL",
            notes=reason,
            user=user,
        )


class StockMovement(TimeStampedModel):
    """Immutable ledger of all physical stock additions, sales, and corrections."""

    class MovementType(models.TextChoices):
        PURCHASE_RECEIPT = "PURCHASE_RECEIPT", "Purchase Receipt"
        ORDER_SALE = "ORDER_SALE", "Order Sale"
        ORDER_CANCEL = "ORDER_CANCEL", "Order Cancellation Return"
        CUSTOMER_RETURN = "CUSTOMER_RETURN", "Customer Return"
        ADJUSTMENT_MANUAL = "ADJUSTMENT_MANUAL", "Manual Adjustment"
        DAMAGE = "DAMAGE", "Damaged / Written Off"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="movements")
    movement_type = models.CharField(max_length=30, choices=MovementType.choices)
    quantity = models.IntegerField(help_text="Positive for additions, negative for deductions")
    reference_id = models.CharField(max_length=120, blank=True, default="")
    notes = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Stock Movement"
        verbose_name_plural = "Stock Movements"

    def __str__(self):
        return f"{self.movement_type}: {self.quantity:+d} units for {self.inventory_item.sku}"


class StockReservation(TimeStampedModel):
    """Temporary hold during checkout process."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name="reservations")
    quantity = models.PositiveIntegerField()
    reference_id = models.CharField(max_length=120, db_index=True)
    is_released = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Hold {self.quantity} of {self.inventory_item.sku} (Ref: {self.reference_id})"
