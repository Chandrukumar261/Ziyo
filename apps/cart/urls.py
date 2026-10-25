from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail_view, name="cart_detail"),
    path("add/<uuid:product_id>/", views.add_to_cart_view, name="add_to_cart"),
    path("update/<uuid:item_id>/", views.update_cart_quantity_view, name="update_quantity"),
    path("remove/<uuid:item_id>/", views.remove_from_cart_view, name="remove_item"),
    path("wishlist/", views.wishlist_view, name="wishlist"),
    path("wishlist/toggle/<uuid:product_id>/", views.toggle_wishlist_view, name="toggle_wishlist"),
]
