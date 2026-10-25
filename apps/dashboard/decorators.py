from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from django.urls import reverse

def management_required(view_func):
    """
    Ensures user is authenticated and has explicit Staff or Store Manager role.
    Ordinary customers get a 403 Forbidden.
    Unauthenticated users get redirected to the dedicated staff login page.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            try:
                login_url = reverse("dashboard:login")
            except Exception:
                login_url = "/login/"
            return redirect(f"{login_url}?next={request.path}")
        if not request.user.is_management_authorized:
            raise PermissionDenied("Access Denied: Administrative authority required.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view
