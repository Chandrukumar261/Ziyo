from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import CustomerRegistrationForm, CustomerLoginForm, UserProfileForm, CustomerAddressForm
from .models import CustomerAddress

def register_view(request):
    """Customer account registration."""
    if request.user.is_authenticated:
        return redirect("catalog:home")

    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Ziyo, {user.first_name or user.email}! Your account was created successfully.")
            return redirect("catalog:home")
    else:
        form = CustomerRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    """Customer account login."""
    if request.user.is_authenticated:
        return redirect("catalog:home")

    next_url = request.GET.get("next") or request.POST.get("next") or "catalog:home"

    if request.method == "POST":
        form = CustomerLoginForm(request.POST, request=request)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.email}!")
            return redirect(next_url)
    else:
        form = CustomerLoginForm()

    return render(request, "accounts/login.html", {"form": form, "next": next_url})


def logout_view(request):
    """Log out customer or staff user."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("catalog:home")


@login_required
def profile_view(request):
    """View and update customer profile."""
    profile = request.user.profile
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile details have been updated.")
            return redirect("accounts:profile")
    else:
        form = UserProfileForm(instance=profile)

    recent_orders = request.user.orders.all().order_by("-created_at")[:5] if hasattr(request.user, "orders") else []
    addresses = request.user.addresses.all()

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "recent_orders": recent_orders,
            "addresses": addresses,
        },
    )


@login_required
def address_list_view(request):
    """Manage customer shipping & billing addresses."""
    addresses = request.user.addresses.all()
    return render(request, "accounts/addresses.html", {"addresses": addresses})


@login_required
def address_create_view(request):
    """Create a new address for the customer."""
    if request.method == "POST":
        form = CustomerAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "New address added successfully.")
            return redirect("accounts:address_list")
    else:
        form = CustomerAddressForm()

    return render(request, "accounts/address_form.html", {"form": form, "title": "Add New Address"})


@login_required
def address_edit_view(request, address_id):
    """Edit an existing address belonging to the customer."""
    address = get_object_or_404(CustomerAddress, id=address_id, user=request.user)
    if request.method == "POST":
        form = CustomerAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully.")
            return redirect("accounts:address_list")
    else:
        form = CustomerAddressForm(instance=address)

    return render(request, "accounts/address_form.html", {"form": form, "title": "Edit Address"})


@login_required
def address_delete_view(request, address_id):
    """Delete a customer address safely."""
    address = get_object_or_404(CustomerAddress, id=address_id, user=request.user)
    if request.method == "POST":
        address.delete()
        messages.success(request, "Address removed successfully.")
        return redirect("accounts:address_list")

    return render(request, "accounts/address_confirm_delete.html", {"address": address})
