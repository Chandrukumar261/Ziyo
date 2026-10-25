from .models import Category

def catalog_context(request):
    """Provides navigation categories to all storefront templates."""
    categories = Category.objects.filter(is_active=True, parent__isnull=True).prefetch_related("children")[:8]
    featured_categories = Category.objects.filter(is_active=True, is_featured=True)[:6]
    return {
        "nav_categories": categories,
        "featured_nav_categories": featured_categories,
    }
