import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.core.models import TimeStampedModel
from apps.catalog.models import Product, ProductVariant

class Order(TimeStampedModel):
    """
    Authoritative order record representing purchased products and delivery commitments.
    """
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAYMENT_PENDING = "PAYMENT_PENDING", "Payment Pending"
        PAID = "PAID", "Paid"
        PROCESSING = "PROCESSING", "Processing"
        SHIPPED = "SHIPPED", "Shipped"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"
        REFUNDED = "REFUNDED", "Refunded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=40, unique=True, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    email = models.EmailField("Customer Email", db_index=True)
    phone = models.CharField("Customer Phone", max_length=20)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    # Server-calculated monetary fields - DecimalField ONLY
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    coupon_code = models.CharField(max_length=50, blank=True, default="")
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    # Shipping Address Snapshot
    shipping_full_name = models.CharField(max_length=150)
    shipping_phone = models.CharField(max_length=20)
    shipping_address_line_1 = models.CharField(max_length=255)
    shipping_address_line_2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100, default="India")

    # Order Notes & Tracking
    customer_notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    tracking_number = models.CharField(max_length=100, blank=True, default="")
    carrier = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.order_number} - {self.email} (₹{self.total_amount})"

    @classmethod
    def generate_order_number(cls):
        """Generates a unique, collision-resistant order number."""
        date_str = timezone.now().strftime("%Y%m%d")
        unique_suffix = uuid.uuid4().hex[:6].upper()
        return f"ZY-{date_str}-{unique_suffix}"

    def update_status(self, new_status, notes="", changed_by=None):
        """Updates status and logs history."""
        self.status = new_status
        self.save()
        OrderStatusHistory.objects.create(
            order=self,
            status=new_status,
            notes=notes,
            changed_by=changed_by,
        )


class OrderItem(TimeStampedModel):
    """
    Immutable line item snapshot of an ordered product, preserving prices and names forever.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
    )
    product_name = models.CharField(max_length=255)
    variant_name = models.CharField(max_length=150, blank=True, default="")
    sku = models.CharField(max_length=80)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in #{self.order.order_number}"


class OrderStatusHistory(TimeStampedModel):
    """Audit log of status changes for an order."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_history")
    status = models.CharField(max_length=25, choices=Order.Status.choices)
    notes = models.CharField(max_length=255, blank=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order Status History"
        verbose_name_plural = "Order Status Histories"

    def __str__(self):
        return f"{self.order.order_number} changed to {self.status}"


class Shipment(TimeStampedModel):
    """Package tracking details for shipped orders."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="shipment")
    carrier = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=120)
    shipped_at = models.DateTimeField(default=timezone.now)
    estimated_delivery = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Shipment for #{self.order.order_number} via {self.carrier}"


class ReturnRequest(TimeStampedModel):
    """Customer return / refund requests."""
    class ReturnStatus(models.TextChoices):
        REQUESTED = "REQUESTED", "Requested"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        COMPLETED = "COMPLETED", "Completed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="return_requests")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=ReturnStatus.choices,
        default=ReturnStatus.REQUESTED,
    )
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Return for #{self.order.order_number} - {self.status}"
