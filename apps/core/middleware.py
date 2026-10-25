from django.conf import settings
from .models import AuditLog

class SecurityHeadersMiddleware:
    """
    Production-grade HTTP Security Headers Enforcement Middleware.
    Applies Content Security Policy (CSP), anti-clickjacking, MIME-sniff protection,
    and privacy/device permission policies on all responses.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Defend against public probes for .env, .git, or sensitive configuration files
        path_segments = [seg.lower() for seg in request.path_info.strip("/").split("/") if seg]
        if any(seg.startswith(".") or seg.endswith((".env", ".key", ".pem", ".sql", ".bak")) for seg in path_segments):
            from django.http import HttpResponseNotFound
            return HttpResponseNotFound("Not Found")

        response = self.get_response(request)

        # 1. Content Security Policy (allows local assets, fonts, CDNs for icons)
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' https://unpkg.com https://cdn.jsdelivr.net https://checkout.razorpay.com",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com data:",
            "img-src 'self' data: https:",
            "frame-src 'self' https://api.razorpay.com https://checkout.razorpay.com",
            "connect-src 'self' https://api.razorpay.com https://lumberjack.razorpay.com",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'",
        ]
        response["Content-Security-Policy"] = "; ".join(csp_directives)

        # 2. MIME Type Sniffing Prevention
        response["X-Content-Type-Options"] = "nosniff"

        # 3. Anti-Clickjacking Frame Protection
        response["X-Frame-Options"] = "DENY"

        # 4. Referrer Policy
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # 5. Browser Permissions Policy
        response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=(), payment=(self)"

        # 6. Cross-Origin Protections
        response["Cross-Origin-Opener-Policy"] = "same-origin"

        return response


class AuditLoggingMiddleware:
    """
    Middleware that records staff actions and sensitive operations into AuditLog.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log mutating actions on /management/ or admin by authenticated staff users
        is_admin_path = (
            request.path.startswith("/management/")
            or request.path.startswith("/django-admin/")
            or (getattr(settings, "ZIYO_PORTAL", "") == "management" and not request.path.startswith("/static/"))
        )
        if (
            is_admin_path
            and request.method in ("POST", "PUT", "PATCH", "DELETE")
            and request.user.is_authenticated
        ):
            ip = self._get_client_ip(request)
            AuditLog.objects.create(
                user=request.user,
                user_email=request.user.email,
                action="UPDATE" if request.method in ("POST", "PUT", "PATCH") else "DELETE",
                resource_type=f"Admin Path: {request.path}",
                resource_id="",
                ip_address=ip,
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:255],
                details={
                    "status_code": response.status_code,
                    "method": request.method,
                },
            )

        return response

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
