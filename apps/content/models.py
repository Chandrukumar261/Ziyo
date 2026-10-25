import uuid
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from apps.core.models import TimeStampedModel

class Banner(TimeStampedModel):
    """Marketing and homepage visual banners."""

    class Location(models.TextChoices):
        HERO = "HERO", "Hero Slider / Top Banner"
        PROMO_GRID = "PROMO_GRID", "Promotional Grid"
        POPUP = "POPUP", "Promotional Popup"
        FOOTER = "FOOTER", "Footer Banner"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="banners/%Y/%m/", null=True, blank=True)
    link_url = models.CharField(max_length=255, default="/products/")
    button_text = models.CharField(max_length=50, default="Explore Now")
    location = models.CharField(
        max_length=25,
        choices=Location.choices,
        default=Location.HERO,
        db_index=True,
    )
    is_active = models.BooleanField(default=True, db_index=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "-created_at"]
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        return f"{self.title} ({self.location})"


class Page(TimeStampedModel):
    """CMS informational pages (About, Terms, Privacy, Shipping, Returns)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, db_index=True)
    content = models.TextField(help_text="Formatted page content")
    meta_description = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Page"
        verbose_name_plural = "Pages"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("content:page_detail", kwargs={"slug": self.slug})


class SiteSetting(TimeStampedModel):
    """Key-value dynamic configuration for store operational parameters."""
    key = models.CharField(max_length=80, unique=True, db_index=True)
    value = models.TextField()
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["key"]
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"{self.key}: {self.value}"

    @classmethod
    def get_val(cls, key, default=""):
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default


class NewsletterSubscription(TimeStampedModel):
    """Newsletter subscriber database."""
    email = models.EmailField(unique=True, db_index=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"

    def __str__(self):
        return self.email
