import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.orders.models import Order

class Payment(TimeStampedModel):
    """Authoritative financial record for a completed or attempted order payment."""

    class Provider(models.TextChoices):
        RAZORPAY = "RAZORPAY", "Razorpay"
        COD = "COD", "Cash on Delivery"
        TEST_SANDBOX = "TEST_SANDBOX", "Test Gateway"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        AUTHORIZED = "AUTHORIZED", "Authorized"
        CAPTURED = "CAPTURED", "Captured"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name="payment")
    provider = models.CharField(max_length=30, choices=Provider.choices, default=Provider.RAZORPAY)
    transaction_id = models.CharField(max_length=120, unique=True, db_index=True)
    gateway_order_id = models.CharField(max_length=120, blank=True, default="", db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    payment_method_type = models.CharField(max_length=50, blank=True, default="")
    raw_response = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"{self.provider} Payment ({self.transaction_id}) for #{self.order.order_number}: ₹{self.amount} [{self.status}]"


class PaymentAttempt(TimeStampedModel):
    """Tracks each payment attempt (e.g. gateway checkout session initialization)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payment_attempts")
    gateway_order_id = models.CharField(max_length=120, db_index=True)
    status = models.CharField(max_length=30, default="INITIATED")
    error_code = models.CharField(max_length=100, blank=True, default="")
    error_description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Attempt {self.gateway_order_id} for #{self.order.order_number} ({self.status})"


class PaymentWebhookEvent(TimeStampedModel):
    """
    Guarantees webhook idempotency and duplicate delivery protection.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.CharField(max_length=150, unique=True, db_index=True)
    event_type = models.CharField(max_length=100, db_index=True)
    provider = models.CharField(max_length=30, default="RAZORPAY")
    payload = models.JSONField()
    is_processed = models.BooleanField(default=False, db_index=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Webhook {self.event_id} ({self.event_type}) - Processed: {self.is_processed}"


class RefundTransaction(TimeStampedModel):
    """Tracks refund transactions initiated by store managers."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name="refunds")
    refund_id = models.CharField(max_length=120, unique=True, db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=30, default="PROCESSED")
    initiated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Refund {self.refund_id} for ₹{self.amount} [{self.status}]"
