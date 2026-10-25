from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Coupon

@require_POST
def apply_coupon_view(request):
    """Applies a coupon code to the active session."""
    code = request.POST.get("code", "").upper().strip()
    if not code:
        messages.error(request, "Please enter a coupon code.")
        return redirect("cart:cart_detail")

    try:
        coupon = Coupon.objects.get(code=code)
    except Coupon.DoesNotExist:
        messages.error(request, f"Coupon '{code}' is invalid.")
        return redirect("cart:cart_detail")

    # Store in session; final validation occurs in cart context and at checkout
    request.session["coupon_code"] = coupon.code
    messages.success(request, f"Coupon '{coupon.code}' applied!")
    return redirect("cart:cart_detail")


@require_POST
def remove_coupon_view(request):
    """Removes the applied coupon code from session."""
    if "coupon_code" in request.session:
        del request.session["coupon_code"]
        messages.info(request, "Coupon removed.")
    return redirect("cart:cart_detail")
