from django.conf import settings
from .models import Page, SiteSetting

def site_settings(request):
    """Provides CMS policy pages, store branding settings, and portal URLs to all templates."""
    footer_pages = Page.objects.filter(is_published=True)[:6]
    return {
        "footer_pages": footer_pages,
        "store_name": SiteSetting.get_val("STORE_NAME", "Ziyo"),
        "store_email": SiteSetting.get_val("STORE_EMAIL", "support@ziyo.store"),
        "store_phone": SiteSetting.get_val("STORE_PHONE", "+91 98765 43210"),
        "store_tagline": SiteSetting.get_val("STORE_TAGLINE", "Curated Essentials, Pure Aesthetics"),
        "STOREFRONT_URL": getattr(settings, "STOREFRONT_URL", "http://127.0.0.1:8000/"),
        "MANAGEMENT_URL": getattr(settings, "MANAGEMENT_URL", "http://127.0.0.1:8001/"),
    }

