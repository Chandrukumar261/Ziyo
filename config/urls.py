"""
URL Configuration for Ziyo E-Commerce Platform.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize Django admin header and title
admin.site.site_header = "Ziyo Technical Administration"
admin.site.site_title = "Ziyo Admin Portal"
admin.site.index_title = "Technical Controls & DB Admin"

urlpatterns = [
    # Technical Django Admin (kept distinct from business management dashboard)
    path("django-admin/", admin.site.urls),

    # Protected Business Administration Interface
    path("management/", include("apps.dashboard.urls", namespace="dashboard")),

    # Customer Storefront Applications
    path("account/", include("apps.accounts.urls", namespace="accounts")),
    path("cart/", include("apps.cart.urls", namespace="cart")),
    path("checkout/", include("apps.orders.checkout_urls", namespace="checkout")),
    path("orders/", include("apps.orders.urls", namespace="orders")),
    path("payments/", include("apps.payments.urls", namespace="payments")),
    path("discounts/", include("apps.discounts.urls", namespace="discounts")),
    path("content/", include("apps.content.urls", namespace="content")),
    path("ai/", include("apps.ai_assistant.urls", namespace="ai_assistant")),

    # Custom REST APIs
    path("api/v1/", include("apps.api.urls", namespace="api_v1")),

    # Catalog & Homepage at root
    path("", include("apps.catalog.urls", namespace="catalog")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom Error Handlers
handler400 = "apps.core.views.bad_request_view"
handler403 = "apps.core.views.permission_denied_view"
handler404 = "apps.core.views.page_not_found_view"
handler500 = "apps.core.views.server_error_view"
