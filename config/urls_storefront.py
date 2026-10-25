"""
URL Configuration for Ziyo Customer Storefront Website.
Completely isolated from the internal management portal.
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Customer Account & Auth
    path("account/", include("apps.accounts.urls", namespace="accounts")),
    
    # Cart & Shopping Bag
    path("cart/", include("apps.cart.urls", namespace="cart")),
    
    # Order Flow & Checkout
    path("checkout/", include("apps.orders.checkout_urls", namespace="checkout")),
    path("orders/", include("apps.orders.urls", namespace="orders")),
    
    # Payment Gateways & Webhooks
    path("payments/", include("apps.payments.urls", namespace="payments")),
    
    # Promotions & Coupons
    path("discounts/", include("apps.discounts.urls", namespace="discounts")),
    
    # CMS Content, Policies, Contact
    path("content/", include("apps.content.urls", namespace="content")),
    
    # AI Customer Concierge Assistant
    path("ai/", include("apps.ai_assistant.urls", namespace="ai_assistant")),

    # Custom REST APIs (Checkout, Payments, Cart, Auth)
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
