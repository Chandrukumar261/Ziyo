from django import forms
from apps.catalog.models import Product, ProductImage, Category, ProductVariant
from apps.discounts.models import Coupon
from apps.content.models import Banner, SiteSetting
from apps.orders.models import Order
from apps.inventory.models import InventoryItem

class ProductAdminForm(forms.ModelForm):
    """Admin form for product creation and updating."""
    class Meta:
        model = Product
        fields = (
            "name",
            "category",
            "sku",
            "price",
            "compare_at_price",
            "cost_price",
            "short_description",
            "description",
            "tags",
            "is_featured",
            "is_trending",
            "is_new_arrival",
            "is_active",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "sku": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "compare_at_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "cost_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "short_description": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5, "id": "product_description_input"}),
            "tags": forms.TextInput(attrs={"class": "form-control", "placeholder": "minimal, linen, natural"}),
            "is_featured": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_trending": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_new_arrival": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ProductImageForm(forms.ModelForm):
    """Admin form to upload product images."""
    class Meta:
        model = ProductImage
        fields = ("image", "alt_text", "is_feature", "sort_order")
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "alt_text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Image description"}),
            "is_feature": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "sort_order": forms.NumberInput(attrs={"class": "form-control"}),
        }


class CategoryAdminForm(forms.ModelForm):
    """Admin form for categories."""
    class Meta:
        model = Category
        fields = ("name", "parent", "description", "image", "is_featured", "is_active", "sort_order")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "parent": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "is_featured": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "sort_order": forms.NumberInput(attrs={"class": "form-control"}),
        }


class CouponAdminForm(forms.ModelForm):
    """Admin form for promotional coupons."""
    class Meta:
        model = Coupon
        fields = (
            "code",
            "discount_type",
            "value",
            "min_purchase_amount",
            "max_discount_amount",
            "usage_limit",
            "per_user_limit",
            "valid_from",
            "valid_to",
            "is_active",
        )
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. SUMMER25"}),
            "discount_type": forms.Select(attrs={"class": "form-select"}),
            "value": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "min_purchase_amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "max_discount_amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "usage_limit": forms.NumberInput(attrs={"class": "form-control"}),
            "per_user_limit": forms.NumberInput(attrs={"class": "form-control"}),
            "valid_from": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "valid_to": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class BannerAdminForm(forms.ModelForm):
    """Admin form for banners."""
    class Meta:
        model = Banner
        fields = ("title", "subtitle", "image", "link_url", "button_text", "location", "is_active", "sort_order")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "subtitle": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "link_url": forms.TextInput(attrs={"class": "form-control"}),
            "button_text": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "sort_order": forms.NumberInput(attrs={"class": "form-control"}),
        }


class OrderFulfillmentForm(forms.Form):
    """Form to update order status, carrier, and tracking number."""
    status = forms.ChoiceField(choices=Order.Status.choices, widget=forms.Select(attrs={"class": "form-select"}))
    carrier = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Blue Dart, DHL"}))
    tracking_number = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Tracking number"}))
    admin_notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Internal fulfillment notes"}))


class StockAdjustmentForm(forms.Form):
    """Form for manual inventory adjustments."""
    quantity_delta = forms.IntegerField(label="Quantity to Add/Deduct", help_text="Use positive to add stock, negative to deduct.", widget=forms.NumberInput(attrs={"class": "form-control"}))
    reason = forms.CharField(label="Reason / Audit Note", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. New shipment receipt batch #948"}))
