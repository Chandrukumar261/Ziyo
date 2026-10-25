from django import forms
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    """Customer product review form."""
    class Meta:
        model = ProductReview
        fields = ("rating", "title", "comment")
        widgets = {
            "rating": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Summarize your review"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "What did you like or dislike about this product?"}),
        }
