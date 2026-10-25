from django.urls import path
from . import views

app_name = "content"

urlpatterns = [
    path("contact/", views.contact_view, name="contact"),
    path("newsletter/subscribe/", views.newsletter_subscribe_view, name="newsletter_subscribe"),
    path("<slug:slug>/", views.page_detail_view, name="page_detail"),
]
