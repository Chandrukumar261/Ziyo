from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Page, NewsletterSubscription

def page_detail_view(request, slug):
    """Informational CMS page (e.g. About, Terms, Privacy Policy)."""
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, "storefront/page_detail.html", {"page": page})


def contact_view(request):
    """Customer contact and inquiry page."""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip() or "Customer Inquiry"
        message_body = request.POST.get("message", "").strip()

        if name and email and message_body:
            # Send notification or log email
            try:
                send_mail(
                    subject=f"[Ziyo Contact] {subject} from {name}",
                    message=f"From: {name} <{email}>\n\nMessage:\n{message_body}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, "Thank you for reaching out! Our team will respond shortly.")
            return redirect("content:contact")
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, "storefront/contact.html")


@require_POST
def newsletter_subscribe_view(request):
    """Add customer email to newsletter subscriber list."""
    email = request.POST.get("email", "").lower().strip()
    if email:
        sub, created = NewsletterSubscription.objects.get_or_create(email=email)
        if not sub.is_active:
            sub.is_active = True
            sub.save()
        messages.success(request, "Thank you for subscribing to Ziyo exclusives!")
    else:
        messages.error(request, "Please enter a valid email address.")

    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "catalog:home"
    return redirect(next_url)
