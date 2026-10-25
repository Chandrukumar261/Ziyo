from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("pay/<str:order_number>/", views.initiate_payment_view, name="initiate_payment"),
    path("cod/<str:order_number>/", views.switch_to_cod_view, name="switch_to_cod"),
    path("callback/", views.payment_callback_view, name="callback"),
    path("failed/<str:order_number>/", views.payment_failure_view, name="payment_failure"),
    path("webhook/razorpay/", views.razorpay_webhook_view, name="razorpay_webhook"),
]
