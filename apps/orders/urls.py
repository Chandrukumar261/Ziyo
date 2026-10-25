from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.order_list_view, name="order_list"),
    path("<str:order_number>/", views.order_detail_view, name="order_detail"),
    path("<str:order_number>/success/", views.order_success_view, name="order_success"),
    path("<str:order_number>/return/", views.return_request_view, name="return_request"),
]
