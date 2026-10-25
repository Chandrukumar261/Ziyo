import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from apps.core.models import TimeStampedModel

class UserManager(BaseUserManager):
    """Custom user manager using email as unique identifier."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")
        email = self.normalize_email(email).lower()
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", User.Role.CUSTOMER)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.SUPERUSER)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model for Ziyo with explicit role-based access control."""

    class Role(models.TextChoices):
        GUEST = "GUEST", "Guest"
        CUSTOMER = "CUSTOMER", "Customer"
        STAFF = "STAFF", "Staff"
        STORE_MANAGER = "STORE_MANAGER", "Store Manager"
        SUPERUSER = "SUPERUSER", "Superuser"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField("Email address", unique=True, db_index=True)
    first_name = models.CharField("First name", max_length=150, blank=True)
    last_name = models.CharField("Last name", max_length=150, blank=True)
    phone = models.CharField("Phone number", max_length=20, blank=True)
    role = models.CharField(
        "User Role",
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
        db_index=True,
    )

    is_staff = models.BooleanField("Staff status", default=False)
    is_active = models.BooleanField("Active", default=True)
    date_joined = models.DateTimeField("Date joined", default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        full = f"{self.first_name} {self.last_name}".strip()
        return full if full else self.email.split("@")[0]

    @property
    def is_management_authorized(self):
        """Checks if user has authority to access /management/ portal."""
        return self.is_active and (
            self.is_superuser
            or self.is_staff
            or self.role in [self.Role.STAFF, self.Role.STORE_MANAGER, self.Role.SUPERUSER]
        )


class UserProfile(TimeStampedModel):
    """Extended customer profile data."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/%Y/%m/", null=True, blank=True)
    bio = models.TextField(blank=True, max_length=500)
    birth_date = models.DateField(null=True, blank=True)
    newsletter_subscribed = models.BooleanField(default=True)
    loyalty_points = models.PositiveIntegerField(default=0)
    preferred_currency = models.CharField(max_length=3, default="INR")

    def __str__(self):
        return f"Profile of {self.user.email}"


class CustomerAddress(TimeStampedModel):
    """Customer shipping and billing addresses."""

    class AddressType(models.TextChoices):
        SHIPPING = "SHIPPING", "Shipping"
        BILLING = "BILLING", "Billing"
        BOTH = "BOTH", "Shipping & Billing"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField("Recipient Full Name", max_length=150)
    phone = models.CharField("Phone Number", max_length=20)
    address_line_1 = models.CharField("Address Line 1", max_length=255)
    address_line_2 = models.CharField("Address Line 2 (Apartment, Suite, etc.)", max_length=255, blank=True)
    city = models.CharField("City", max_length=100)
    state = models.CharField("State / Province", max_length=100)
    postal_code = models.CharField("Postal / ZIP Code", max_length=20)
    country = models.CharField("Country", max_length=100, default="India")
    address_type = models.CharField(
        max_length=15,
        choices=AddressType.choices,
        default=AddressType.SHIPPING,
    )
    is_default = models.BooleanField("Set as Default", default=False)

    class Meta:
        ordering = ["-is_default", "-created_at"]
        verbose_name = "Customer Address"
        verbose_name_plural = "Customer Addresses"

    def __str__(self):
        return f"{self.full_name} - {self.address_line_1}, {self.city}"

    def save(self, *args, **kwargs):
        if self.is_default:
            CustomerAddress.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
