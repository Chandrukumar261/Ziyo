import uuid
from django.db import models
from django.conf import settings

class TimeStampedModel(models.Model):
    """Abstract base model with created and modified timestamps."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditLog(models.Model):
    """
    Tracks administrative and sensitive system operations for cybersecurity compliance.
    """
    ACTION_CHOICES = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("LOGIN_FAILED", "Login Failed"),
        ("PAYMENT_ATTEMPT", "Payment Attempt"),
        ("PAYMENT_SUCCESS", "Payment Success"),
        ("PAYMENT_FAILED", "Payment Failed"),
        ("REFUND_ISSUED", "Refund Issued"),
        ("INVENTORY_CHANGE", "Inventory Change"),
        ("EXPORT_DATA", "Export Data"),
        ("SECURITY_EVENT", "Security Event"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    user_email = models.EmailField(blank=True, default="")
    action = models.CharField(max_length=40, choices=ACTION_CHOICES, db_index=True)
    resource_type = models.CharField(max_length=80, db_index=True)
    resource_id = models.CharField(max_length=120, blank=True, default="")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True, default="")
    details = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        user_str = self.user_email or (self.user.email if self.user else "Anonymous")
        return f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] {self.action} on {self.resource_type} by {user_str}"
