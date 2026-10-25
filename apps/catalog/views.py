from decimal import Decimal, InvalidOperation
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Avg, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Product, ProductReview
from .forms import ProductReviewForm
from apps.content.models import Banner

def home_view(request):
    """Ziyo homepage with warm aesthetics, hero banner, featured categories, and trending products."""
    banners = Banner.objects.filter(is_active=True, location=Banner.Location.HERO)[:3]
    featured_categories = Category.objects.filter(is_active=True, is_featured=True)[:6]
    trending_products = (
        Product.active.filter(is_trending=True)
        .prefetch_related("images")
        .select_related("category")[:8]
    )
    new_arrivals = (
        Product.active.filter(is_new_arrival=True)
        .prefetch_related("images")
        .select_related("category")[:8]
    )
    recommended = (
        Product.active.filter(is_featured=True)
        .prefetch_related("images")
        .select_related("category")[:4]
    )

    return render(
        request,
        "storefront/home.html",
        {
            "banners": banners,
            "featured_categories": featured_categories,
            "trending_products": trending_products,
            "new_arrivals": new_arrivals,
            "recommended": recommended,
        },
    )


def product_list_view(request):
    """Product catalog with search, category filter, price filtering, sorting, and pagination."""
    products = Product.active.prefetch_related("images").select_related("category")

    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    in_stock_only = request.GET.get("in_stock", "").strip()
    sort = request.GET.get("sort", "newest")

    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(
            Q(category=selected_category) | Q(category__parent=selected_category)
        )

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(short_description__icontains=query)
            | Q(description__icontains=query)
            | Q(tags__icontains=query)
            | Q(category__name__icontains=query)
        )

    if min_price:
        try:
            products = products.filter(price__gte=Decimal(min_price))
        except (InvalidOperation, ValueError):
            pass

    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except (InvalidOperation, ValueError):
            pass

    # Sorting
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "popular":
        products = products.annotate(num_reviews=Count("reviews")).order_by("-num_reviews", "-price")
    else:  # newest
        products = products.order_by("-created_at")

    # Pagination: 12 products per page
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    try:
        page_obj = paginator.get_page(page_number)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.get_page(1)

    categories = Category.objects.filter(is_active=True, parent__isnull=True).prefetch_related("children")

    return render(
        request,
        "storefront/product_list.html",
        {
            "page_obj": page_obj,
            "products": page_obj.object_list,
            "query": query,
            "selected_category": selected_category,
            "categories": categories,
            "current_sort": sort,
            "min_price": min_price,
            "max_price": max_price,
            "total_count": paginator.count,
        },
    )


def category_detail_view(request, slug):
    """View products within a specific category."""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.active.filter(
        Q(category=category) | Q(category__parent=category)
    ).prefetch_related("images").select_related("category")

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return render(
        request,
        "storefront/category_detail.html",
        {
            "category": category,
            "page_obj": page_obj,
            "products": page_obj.object_list,
        },
    )


def product_detail_view(request, slug):
    """Detailed view for a single product with gallery, variants, reviews, and related products."""
    product = get_object_or_404(
        Product.objects.prefetch_related("images", "variants", "reviews__user").select_related("category"),
        slug=slug,
        is_active=True,
        is_archived=False,
    )

    related_products = (
        Product.active.filter(category=product.category)
        .exclude(pk=product.pk)
        .prefetch_related("images")[:4]
    )

    approved_reviews = product.reviews.filter(is_approved=True)
    review_form = ProductReviewForm() if request.user.is_authenticated else None

    # Check if user already reviewed
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = approved_reviews.filter(user=request.user).exists()

    return render(
        request,
        "storefront/product_detail.html",
        {
            "product": product,
            "images": product.images.all(),
            "variants": product.variants.filter(is_active=True),
            "related_products": related_products,
            "reviews": approved_reviews,
            "review_form": review_form,
            "user_has_reviewed": user_has_reviewed,
        },
    )


@login_required
def add_review_view(request, slug):
    """Submit a customer review for a product."""
    product = get_object_or_404(Product, slug=slug, is_active=True)

    if request.method == "POST":
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            # Check existing review
            review, created = ProductReview.objects.get_or_create(
                product=product,
                user=request.user,
                defaults={
                    "rating": form.cleaned_data["rating"],
                    "title": form.cleaned_data["title"],
                    "comment": form.cleaned_data["comment"],
                    "is_approved": True,
                },
            )
            if not created:
                review.rating = form.cleaned_data["rating"]
                review.title = form.cleaned_data["title"]
                review.comment = form.cleaned_data["comment"]
                review.save()
                messages.success(request, "Your product review has been updated.")
            else:
                messages.success(request, "Thank you! Your review has been posted.")

    return redirect("catalog:product_detail", slug=slug)
