from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test
from .gemini_service import GeminiService

def is_staff_check(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser or user.role in ["STAFF", "STORE_MANAGER", "SUPERUSER"])

@require_POST
def support_chat_view(request):
    """Customer concierge chat response endpoint."""
    user_message = request.POST.get("message", "").strip()
    if not user_message:
        return JsonResponse({"reply": "How can I help you today with your Ziyo experience?"})

    service = GeminiService()
    reply = service.customer_support_assistant(user_message)
    return JsonResponse({"reply": reply})


@user_passes_test(is_staff_check)
@require_POST
def generate_description_preview(request):
    """Administrative assistance for copywriting (requires staff approval)."""
    product_name = request.POST.get("name", "").strip()
    category_name = request.POST.get("category", "").strip()
    attributes = request.POST.get("attributes", "").strip()

    if not product_name:
        return JsonResponse({"error": "Product name is required."}, status=400)

    service = GeminiService()
    description = service.generate_product_description(
        product_name=product_name,
        category_name=category_name,
        attributes=attributes,
    )
    return JsonResponse({"description": description})
