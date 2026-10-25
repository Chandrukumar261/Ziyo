from django.conf import settings
from django.shortcuts import render

def _is_management_portal(request):
    urlconf = getattr(request, "urlconf", None) or getattr(settings, "ROOT_URLCONF", "")
    return (
        "urls_management" in str(urlconf)
        or getattr(settings, "ZIYO_PORTAL", "") == "management"
    )

def bad_request_view(request, exception=None):
    if _is_management_portal(request):
        return render(request, "admin_dashboard/errors/400.html", status=400)
    return render(request, "errors/400.html", status=400)

def permission_denied_view(request, exception=None):
    if _is_management_portal(request):
        return render(request, "admin_dashboard/errors/403.html", status=403)
    return render(request, "errors/403.html", status=403)

def page_not_found_view(request, exception=None):
    if _is_management_portal(request):
        return render(request, "admin_dashboard/errors/404.html", status=404)
    return render(request, "errors/404.html", status=404)

def server_error_view(request):
    if _is_management_portal(request):
        return render(request, "admin_dashboard/errors/500.html", status=500)
    return render(request, "errors/500.html", status=500)
