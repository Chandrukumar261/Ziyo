from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, UserProfile, CustomerAddress

class CustomerRegistrationForm(forms.ModelForm):
    """Secure customer registration form with password confirmation."""
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter secure password (min 8 chars)", "class": "form-control"}),
        help_text="Must be at least 8 characters.",
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Re-enter password", "class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone")
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "name@example.com", "class": "form-control"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First name", "class": "form-control"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name", "class": "form-control"}),
            "phone": forms.TextInput(attrs={"placeholder": "+91 9876543210", "class": "form-control"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email", "").lower().strip()
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        if password:
            validate_password(password)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = User.Role.CUSTOMER
        if commit:
            user.save()
        return user


class CustomerLoginForm(forms.Form):
    """Customer authentication form."""
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={"placeholder": "name@example.com", "class": "form-control"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password", "class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email", "").lower().strip()
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise ValidationError("Invalid email or password.")
            elif not self.user_cache.is_active:
                raise ValidationError("This account is currently deactivated.")

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class UserProfileForm(forms.ModelForm):
    """Profile editing form."""
    first_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = UserProfile
        fields = ("bio", "birth_date", "newsletter_subscribed")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3, "class": "form-control", "placeholder": "A brief bio about you"}),
            "birth_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "newsletter_subscribed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["phone"].initial = self.instance.user.phone

    def save(self, commit=True):
        profile = super().save(commit=commit)
        user = profile.user
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.phone = self.cleaned_data["phone"]
        if commit:
            user.save()
        return profile


class CustomerAddressForm(forms.ModelForm):
    """Address management form."""
    class Meta:
        model = CustomerAddress
        fields = (
            "full_name",
            "phone",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "country",
            "address_type",
            "is_default",
        )
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Recipient Full Name"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+91 9876543210"}),
            "address_line_1": forms.TextInput(attrs={"class": "form-control", "placeholder": "Street address, building, house no."}),
            "address_line_2": forms.TextInput(attrs={"class": "form-control", "placeholder": "Apartment, suite, unit (optional)"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "State / Province"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "PIN / Postal Code"}),
            "country": forms.TextInput(attrs={"class": "form-control", "placeholder": "Country"}),
            "address_type": forms.Select(attrs={"class": "form-select"}),
            "is_default": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
