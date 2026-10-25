import uuid
from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from apps.core.models import TimeStampedModel

class Category(TimeStampedModel):
    """Product hierarchical categories."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True, db_index=True)
    slug = models.SlugField(max_length=180, unique=True, db_index=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/%Y/%m/", null=True, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["sort_order", "name"]

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:category_detail", kwargs={"slug": self.slug})


class ActiveProductManager(models.Manager):
    """Manager returning active, non-archived products."""
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_archived=False)


class Product(TimeStampedModel):
    """Core product model supporting variants, pricing, and stock status."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=280, unique=True, db_index=True)
    sku = models.CharField(max_length=80, unique=True, db_index=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    
    # Financial fields - DecimalField ONLY, never float
    price = models.DecimalField(max_digits=12, decimal_places=2, db_index=True)
    compare_at_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Original price for discount display strike-through"
    )
    cost_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Internal cost for margin tracking"
    )

    is_featured = models.BooleanField(default=False, db_index=True)
    is_trending = models.BooleanField(default=False, db_index=True)
    is_new_arrival = models.BooleanField(default=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    is_archived = models.BooleanField(default=False, db_index=True)  # Soft deletion

    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")

    objects = models.Manager()
    active = ActiveProductManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            candidate = base_slug
            counter = 1
            while Product.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:product_detail", kwargs={"slug": self.slug})

    @property
    def primary_image_url(self):
        primary = self.images.filter(is_feature=True).first() or self.images.first()
        if primary and primary.image:
            return primary.image.url
        return "/static/images/placeholder-product.svg"

    @property
    def discount_percentage(self):
        if self.compare_at_price and self.compare_at_price > self.price:
            saving = self.compare_at_price - self.price
            return int(round((saving / self.compare_at_price) * 100))
        return 0

    @property
    def average_rating(self):
        approved = self.reviews.filter(is_approved=True)
        if not approved.exists():
            return 5.0
        avg = approved.aggregate(models.Avg("rating"))["rating__avg"]
        return round(avg, 1) if avg else 5.0

    @property
    def review_count(self):
        return self.reviews.filter(is_approved=True).count()

    @property
    def total_stock(self):
        """Sum of all inventory items for this product."""
        if hasattr(self, "inventory"):
            return self.inventory.available_quantity
        total = sum(v.inventory.available_quantity for v in self.variants.all() if hasattr(v, "inventory"))
        return total

    @property
    def is_in_stock(self):
        if hasattr(self, "inventory"):
            return self.inventory.available_quantity > 0
        variants = self.variants.all()
        if variants.exists():
            return any(hasattr(v, "inventory") and v.inventory.available_quantity > 0 for v in variants)
        return True


class ProductImage(TimeStampedModel):
    """Multiple product gallery images."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/%Y/%m/")
    alt_text = models.CharField(max_length=255, blank=True)
    is_feature = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "-is_feature", "created_at"]

    def __str__(self):
        return f"Image for {self.product.name}"

    def save(self, *args, **kwargs):
        if self.is_feature:
            ProductImage.objects.filter(product=self.product, is_feature=True).exclude(pk=self.pk).update(is_feature=False)
        super().save(*args, **kwargs)


class ProductAttribute(TimeStampedModel):
    """Variant attributes (e.g., Color, Size, Material)."""
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductVariant(TimeStampedModel):
    """Specific SKU variation of a parent product."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    name = models.CharField(max_length=150, help_text="e.g. Oatmeal Cream / Medium")
    sku = models.CharField(max_length=80, unique=True, db_index=True)
    price_override = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Optional variant price override"
    )
    attributes = models.JSONField(default=dict, blank=True, help_text="e.g. {'color': 'Cream', 'size': 'M'}")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.product.name} - {self.name} ({self.sku})"

    @property
    def price(self):
        return self.price_override if self.price_override is not None else self.product.price


class ProductReview(TimeStampedModel):
    """Customer ratings and reviews for verified products."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(choices=[(i, f"{i} Stars") for i in range(1, 6)], default=5)
    title = models.CharField(max_length=150)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True, db_index=True)  # Auto-approved or moderation

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.rating}* by {self.user.email} on {self.product.name}"
