import re
from django import forms
from django.core.exceptions import ValidationError
from .models import ReturnRequest
from apps.core.countries import COUNTRIES

class CheckoutForm(forms.Form):
    """Customer checkout information form with global country and payment method selection."""

    PAYMENT_METHOD_CHOICES = (
        ("RAZORPAY_CARD", "Credit / Debit Card (Visa, MasterCard, RuPay, Amex)"),
        ("RAZORPAY_UPI", "UPI / Net Banking / Wallets (Razorpay)"),
        ("COD", "Cash on Delivery (Pay in cash or UPI upon delivery)"),
    )

    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
    )
    phone = forms.CharField(
        label="Phone Number",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "+91 9876543210"}),
    )
    full_name = forms.CharField(
        label="Recipient Full Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Full Name"}),
    )
    country = forms.ChoiceField(
        label="Country / Region",
        choices=COUNTRIES,
        initial="IN",
        required=False,
        widget=forms.Select(attrs={"class": "form-control", "id": "id_country"}),
    )
    address_line_1 = forms.CharField(
        label="Address Line 1",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "House/Flat number, Street"}),
    )
    address_line_2 = forms.CharField(
        label="Address Line 2 (Optional)",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Apartment, suite, unit"}),
    )
    city = forms.CharField(
        label="City",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
    )
    state = forms.CharField(
        label="State / Province",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "State or Province"}),
    )
    postal_code = forms.CharField(
        label="PIN / Postal Code",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Postal Code", "id": "id_postal_code"}),
    )
    payment_method = forms.ChoiceField(
        label="Payment Method",
        choices=PAYMENT_METHOD_CHOICES,
        initial="RAZORPAY_CARD",
        required=False,
        widget=forms.RadioSelect(attrs={"class": "payment-method-radio"}),
    )
    customer_notes = forms.CharField(
        label="Order Notes (Optional)",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Special instructions for delivery"}),
    )

    def clean_country(self):
        return self.cleaned_data.get("country") or "IN"

    def clean_payment_method(self):
        return self.cleaned_data.get("payment_method") or "RAZORPAY_CARD"

    def clean_postal_code(self):
        country = self.cleaned_data.get("country", "IN")
        postal_code = self.cleaned_data.get("postal_code", "").strip()

        if country == "IN":
            # 6-digit Indian PIN code
            cleaned_pin = re.sub(r"\s+", "", postal_code)
            if not re.match(r"^[1-9][0-9]{5}$", cleaned_pin):
                raise ValidationError("Please enter a valid 6-digit Indian PIN code (e.g. 560001, 110001).")
            return cleaned_pin

        # International postal code: allow 3 to 10 alphanumeric characters and hyphens/spaces
        cleaned_intl = postal_code.strip()
        if not re.match(r"^[A-Za-z0-9\s\-]{3,10}$", cleaned_intl):
            raise ValidationError("Please enter a valid postal or ZIP code.")
        return cleaned_intl


class ReturnRequestForm(forms.ModelForm):
    """Customer return request submission."""
    class Meta:
        model = ReturnRequest
        fields = ("reason",)
        widgets = {
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Please describe why you would like to return this order."}),
        }
