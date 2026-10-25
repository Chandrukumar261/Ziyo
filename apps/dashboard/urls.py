from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    # Auth
    path("login/", views.admin_login_view, name="login"),

    # Overview
    path("", views.dashboard_overview, name="overview"),

    # Products CRUD
    path("products/", views.product_list, name="product_list"),
    path("products/create/", views.product_create, name="product_create"),
    path("products/<uuid:product_id>/edit/", views.product_edit, name="product_edit"),
    path("products/<uuid:product_id>/delete/", views.product_delete, name="product_delete"),
    path("products/<uuid:product_id>/images/", views.product_images, name="product_images"),
    path("products/images/<uuid:image_id>/delete/", views.delete_product_image, name="delete_product_image"),

    # Categories CRUD
    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.category_create, name="category_create"),
    path("categories/<uuid:category_id>/edit/", views.category_edit, name="category_edit"),
    path("categories/<uuid:category_id>/delete/", views.category_delete, name="category_delete"),

    # Order Management & Fulfillment
    path("orders/", views.order_list, name="order_list"),
    path("orders/<uuid:order_id>/", views.order_detail, name="order_detail"),

    # Inventory Supervision
    path("inventory/", views.inventory_list, name="inventory_list"),
    path("inventory/<uuid:item_id>/adjust/", views.inventory_adjust, name="inventory_adjust"),

    # Coupons CRUD
    path("coupons/", views.coupon_list, name="coupon_list"),
    path("coupons/create/", views.coupon_create, name="coupon_create"),
    path("coupons/<uuid:coupon_id>/edit/", views.coupon_edit, name="coupon_edit"),
    path("coupons/<uuid:coupon_id>/delete/", views.coupon_delete, name="coupon_delete"),

    # Review Moderation
    path("reviews/", views.review_list, name="review_list"),
    path("reviews/<uuid:review_id>/toggle/", views.review_toggle_approval, name="review_toggle"),

    # Banners CRUD
    path("banners/", views.banner_list, name="banner_list"),
    path("banners/create/", views.banner_create, name="banner_create"),
    path("banners/<uuid:banner_id>/edit/", views.banner_edit, name="banner_edit"),
    path("banners/<uuid:banner_id>/delete/", views.banner_delete, name="banner_delete"),

    # Customers & CRM
    path("customers/", views.customer_list, name="customer_list"),
    path("customers/<uuid:customer_id>/", views.customer_detail, name="customer_detail"),

    # Audit Logs
    path("audit/", views.audit_log_list, name="audit_log_list"),

    # Store Settings
    path("settings/", views.store_settings_view, name="settings"),
]
