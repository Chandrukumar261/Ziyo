"""
URL Configuration for Ziyo Dedicated Management & Administration Website.
Runs on an isolated administrative port and domain.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.dashboard import views as dashboard_views

# Configure Django Technical Admin headers
admin.site.site_header = "Ziyo Technical Administration"
admin.site.site_title = "Ziyo Admin Portal"
admin.site.index_title = "Technical Controls & DB Admin"

urlpatterns = [
    # Technical Django DB Admin (Accessible securely on management host only)
    path("django-admin/", admin.site.urls),

    # Staff Authentication
    path("account/", include("apps.accounts.urls", namespace="accounts")),

    # AI Operations & Copywriting Assistant
    path("ai/", include("apps.ai_assistant.urls", namespace="ai_assistant")),

    # Management Portal at Root
    path("", include("apps.dashboard.urls", namespace="dashboard")),

    # Alias /management/ for backward compatibility
    path("management/", include("apps.dashboard.urls")),

    # Management & Staff REST APIs
    path("api/v1/", include("apps.api.urls", namespace="api_v1")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom Error Handlers
handler400 = "apps.core.views.bad_request_view"
handler403 = "apps.core.views.permission_denied_view"
handler404 = "apps.core.views.page_not_found_view"
handler500 = "apps.core.views.server_error_view"
