from django.urls import path
from . import views

app_name = "ai_assistant"

urlpatterns = [
    path("chat/", views.support_chat_view, name="chat"),
    path("admin/generate-description/", views.generate_description_preview, name="generate_description"),
]
