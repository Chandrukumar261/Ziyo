from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from . import views

app_name = "api_v1"

urlpatterns = [
    # 0. Interactive OpenAPI Schema & Swagger UI
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="api_v1:schema"), name="swagger_ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="api_v1:schema"), name="redoc"),

    # 1. Checkout & Payment Security
    path("checkout/order/", views.CheckoutOrderCreateAPIView.as_view(), name="checkout_order_create"),
    path("payments/verify/", views.PaymentVerifyAPIView.as_view(), name="payment_verify"),
    path("payments/webhook/", views.PaymentWebhookAPIView.as_view(), name="payment_webhook"),

    # 2. Server Authoritative Cart
    path("cart/", views.CartAPIView.as_view(), name="cart_detail"),
    path("cart/items/", views.CartAPIView.as_view(), name="cart_add_item"),
    path("cart/items/<uuid:item_id>/", views.CartItemDeleteAPIView.as_view(), name="cart_delete_item"),

    # 3. Authentication & Account
    path("auth/register/", views.AuthRegisterAPIView.as_view(), name="auth_register"),
    path("auth/login/", views.AuthLoginAPIView.as_view(), name="auth_login"),
    path("auth/logout/", views.AuthLogoutAPIView.as_view(), name="auth_logout"),
    path("auth/profile/", views.AuthProfileAPIView.as_view(), name="auth_profile"),

    # 4. Customer Orders & Live Tracking
    path("orders/", views.CustomerOrderListAPIView.as_view(), name="customer_orders"),
    path("orders/<str:order_number>/", views.CustomerOrderDetailAPIView.as_view(), name="customer_order_detail"),
    path("orders/track/<str:order_number>/", views.OrderLiveTrackingAPIView.as_view(), name="order_live_tracking"),
    path("orders/<str:order_number>/shipping-address/", views.OrderShippingAddressUpdateAPIView.as_view(), name="order_shipping_address_update"),

    # 5. External ERP & 3PL Logistics Webhooks
    path("erp/inventory/bulk-sync/", views.ErpBulkInventorySyncAPIView.as_view(), name="erp_inventory_bulk_sync"),
    path("erp/logistics/dispatch/", views.LogisticsDispatchAPIView.as_view(), name="erp_logistics_dispatch"),
    path("erp/webhooks/listener/", views.ErpGenericWebhookListenerAPIView.as_view(), name="erp_generic_webhook"),

    # 6. Protected Administration & RBAC APIs
    path("admin/products/", views.AdminProductListCreateAPIView.as_view(), name="admin_products"),
    path("admin/inventory/adjust/", views.AdminInventoryAdjustAPIView.as_view(), name="admin_inventory_adjust"),
    path("admin/orders/", views.AdminOrderListAPIView.as_view(), name="admin_orders"),
    path("admin/orders/<uuid:order_id>/status/", views.AdminOrderStatusUpdateAPIView.as_view(), name="admin_order_status"),
]
