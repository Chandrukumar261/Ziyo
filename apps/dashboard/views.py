from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.utils import timezone
from django.db import models
from django.db.models import Sum, Count, Q, F
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .decorators import management_required
from .forms import (
    ProductAdminForm,
    ProductImageForm,
    CategoryAdminForm,
    CouponAdminForm,
    BannerAdminForm,
    OrderFulfillmentForm,
    StockAdjustmentForm,
)
from apps.accounts.forms import CustomerLoginForm
from apps.accounts.models import User
from apps.catalog.models import Product, ProductImage, Category, ProductReview
from apps.orders.models import Order, OrderItem
from apps.inventory.models import InventoryItem, StockMovement
from apps.discounts.models import Coupon
from apps.content.models import Banner, SiteSetting
from apps.core.models import AuditLog

def admin_login_view(request):
    """Dedicated management login view."""
    if request.user.is_authenticated and request.user.is_management_authorized:
        return redirect("dashboard:overview")

    next_url = request.GET.get("next") or reverse("dashboard:overview")
    if request.method == "POST":
        form = CustomerLoginForm(request.POST, request=request)
        if form.is_valid():
            user = form.get_user()
            if user.is_management_authorized:
                login(request, user)
                messages.success(request, f"Welcome to Ziyo Management, {user.first_name or user.email}.")
                return redirect(next_url)
            else:
                messages.error(request, "Access restricted: Staff credentials required.")
    else:
        form = CustomerLoginForm()

    return render(request, "admin_dashboard/login.html", {"form": form})


@management_required
def dashboard_overview(request):
    """Executive KPI metrics, sales summaries, and operational alerts."""
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Financial Aggregations
    paid_orders = Order.objects.filter(status__in=[Order.Status.PAID, Order.Status.PROCESSING, Order.Status.SHIPPED, Order.Status.DELIVERED])
    total_revenue = paid_orders.aggregate(total=Sum("total_amount"))["total"] or Decimal("0.00")
    today_revenue = paid_orders.filter(created_at__gte=today_start).aggregate(total=Sum("total_amount"))["total"] or Decimal("0.00")

    total_orders_count = Order.objects.count()
    pending_fulfillment_count = Order.objects.filter(status__in=[Order.Status.PAID, Order.Status.PROCESSING]).count()
    total_customers_count = User.objects.filter(role=User.Role.CUSTOMER).count()

    # Low stock alert
    low_stock_items = InventoryItem.objects.filter(
        quantity_on_hand__lte=models.F("reserved_quantity") + models.F("low_stock_threshold")
    ).select_related("product")[:5]

    recent_orders = Order.objects.select_related("user").order_by("-created_at")[:8]
    recent_audit_logs = AuditLog.objects.order_by("-timestamp")[:6]

    return render(
        request,
        "admin_dashboard/overview.html",
        {
            "total_revenue": total_revenue,
            "today_revenue": today_revenue,
            "total_orders_count": total_orders_count,
            "pending_fulfillment_count": pending_fulfillment_count,
            "total_customers_count": total_customers_count,
            "low_stock_items": low_stock_items,
            "recent_orders": recent_orders,
            "recent_audit_logs": recent_audit_logs,
        },
    )


# ==================== PRODUCT CRUD ====================

@management_required
def product_list(request):
    """List products with search, stock status, and filters."""
    query = request.GET.get("q", "").strip()
    products = Product.objects.filter(is_archived=False).select_related("category", "inventory").order_by("-created_at")

    if query:
        products = products.filter(Q(name__icontains=query) | Q(sku__icontains=query) | Q(category__name__icontains=query))

    paginator = Paginator(products, 15)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return render(request, "admin_dashboard/products/list.html", {"page_obj": page_obj, "query": query})


@management_required
def product_create(request):
    """Create a new product."""
    if request.method == "POST":
        form = ProductAdminForm(request.POST)
        if form.is_valid():
            product = form.save()
            initial_stock = request.POST.get("initial_stock", "0")
            try:
                stock_qty = max(0, int(initial_stock))
            except ValueError:
                stock_qty = 0

            # Create InventoryItem
            InventoryItem.objects.create(
                product=product,
                sku=product.sku,
                quantity_on_hand=stock_qty,
            )

            messages.success(request, f"Product '{product.name}' created successfully.")
            return redirect("dashboard:product_images", product_id=product.id)
    else:
        form = ProductAdminForm()

    return render(request, "admin_dashboard/products/form.html", {"form": form, "title": "Create Product"})


@management_required
def product_edit(request, product_id):
    """Edit existing product."""
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductAdminForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated successfully.")
            return redirect("dashboard:product_list")
    else:
        form = ProductAdminForm(instance=product)

    return render(request, "admin_dashboard/products/form.html", {"form": form, "product": product, "title": f"Edit {product.name}"})


@management_required
def product_delete(request, product_id):
    """Soft delete / archive product so order records remain intact."""
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.is_archived = True
        product.is_active = False
        product.save()
        messages.success(request, f"Product '{product.name}' has been archived.")
        return redirect("dashboard:product_list")

    return render(request, "admin_dashboard/products/confirm_delete.html", {"product": product})


@management_required
def product_images(request, product_id):
    """Manage gallery images for a product."""
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.product = product
            img.save()
            messages.success(request, "Image uploaded successfully.")
            return redirect("dashboard:product_images", product_id=product.id)
    else:
        form = ProductImageForm()

    images = product.images.all()
    return render(request, "admin_dashboard/products/images.html", {"product": product, "form": form, "images": images})


@management_required
@require_POST
def delete_product_image(request, image_id):
    """Delete a single product gallery image."""
    image = get_object_or_404(ProductImage, id=image_id)
    product_id = image.product.id
    image.delete()
    messages.info(request, "Image deleted.")
    return redirect("dashboard:product_images", product_id=product_id)


# ==================== CATEGORY CRUD ====================

@management_required
def category_list(request):
    """List all categories."""
    categories = Category.objects.annotate(num_products=Count("products")).order_by("sort_order", "name")
    return render(request, "admin_dashboard/categories/list.html", {"categories": categories})


@management_required
def category_create(request):
    """Create a new category."""
    if request.method == "POST":
        form = CategoryAdminForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f"Category '{cat.name}' created.")
            return redirect("dashboard:category_list")
    else:
        form = CategoryAdminForm()

    return render(request, "admin_dashboard/categories/form.html", {"form": form, "title": "Create Category"})


@management_required
def category_edit(request, category_id):
    """Edit existing category."""
    cat = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        form = CategoryAdminForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{cat.name}' updated.")
            return redirect("dashboard:category_list")
    else:
        form = CategoryAdminForm(instance=cat)

    return render(request, "admin_dashboard/categories/form.html", {"form": form, "title": f"Edit {cat.name}"})


@management_required
def category_delete(request, category_id):
    """Delete category safely."""
    cat = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        if cat.products.exists():
            messages.error(request, f"Cannot delete '{cat.name}': it contains active products.")
            return redirect("dashboard:category_list")
        cat.delete()
        messages.success(request, f"Category '{cat.name}' deleted.")
        return redirect("dashboard:category_list")

    return render(request, "admin_dashboard/categories/confirm_delete.html", {"category": cat})


# ==================== ORDER FULFILLMENT ====================

@management_required
def order_list(request):
    """List customer orders with status filtering."""
    status_filter = request.GET.get("status", "")
    query = request.GET.get("q", "").strip()

    orders = Order.objects.select_related("user").order_by("-created_at")
    if status_filter:
        orders = orders.filter(status=status_filter)
    if query:
        orders = orders.filter(Q(order_number__icontains=query) | Q(email__icontains=query) | Q(shipping_full_name__icontains=query))

    paginator = Paginator(orders, 20)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return render(request, "admin_dashboard/orders/list.html", {"page_obj": page_obj, "status_filter": status_filter, "query": query, "statuses": Order.Status.choices})


@management_required
def order_detail(request, order_id):
    """Order inspection and fulfillment management."""
    order = get_object_or_404(Order.objects.prefetch_related("items", "status_history"), id=order_id)
    if request.method == "POST":
        form = OrderFulfillmentForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data["status"]
            carrier = form.cleaned_data["carrier"]
            tracking = form.cleaned_data["tracking_number"]
            notes = form.cleaned_data["admin_notes"]

            order.carrier = carrier
            order.tracking_number = tracking
            order.update_status(
                new_status=new_status,
                notes=f"{notes} (Carrier: {carrier}, Tracking: {tracking})".strip(),
                changed_by=request.user,
            )
            messages.success(request, f"Order #{order.order_number} status updated to {new_status}.")
            return redirect("dashboard:order_detail", order_id=order.id)
    else:
        form = OrderFulfillmentForm(initial={
            "status": order.status,
            "carrier": order.carrier,
            "tracking_number": order.tracking_number,
        })

    return render(request, "admin_dashboard/orders/detail.html", {"order": order, "form": form})


# ==================== INVENTORY SUPERVISION ====================

@management_required
def inventory_list(request):
    """List inventory items, available vs reserved stock, and adjustments."""
    items = InventoryItem.objects.select_related("product").order_by("quantity_on_hand")
    return render(request, "admin_dashboard/inventory/list.html", {"items": items})


@management_required
def inventory_adjust(request, item_id):
    """Manually adjust stock for receipt or inventory correction."""
    item = get_object_or_404(InventoryItem, id=item_id)
    if request.method == "POST":
        form = StockAdjustmentForm(request.POST)
        if form.is_valid():
            delta = form.cleaned_data["quantity_delta"]
            reason = form.cleaned_data["reason"]
            item.adjust_stock(delta, reason=reason, user=request.user)
            messages.success(request, f"Stock updated for {item.sku}. New on-hand: {item.quantity_on_hand}")
            return redirect("dashboard:inventory_list")
    else:
        form = StockAdjustmentForm()

    movements = item.movements.all().order_by("-created_at")[:10]
    return render(request, "admin_dashboard/inventory/adjust.html", {"item": item, "form": form, "movements": movements})


# ==================== COUPONS ====================

@management_required
def coupon_list(request):
    """List promotional coupons."""
    coupons = Coupon.objects.annotate(redemptions_count=Count("redemptions")).order_by("-created_at")
    return render(request, "admin_dashboard/coupons/list.html", {"coupons": coupons})


@management_required
def coupon_create(request):
    """Create a coupon."""
    if request.method == "POST":
        form = CouponAdminForm(request.POST)
        if form.is_valid():
            coupon = form.save()
            messages.success(request, f"Coupon '{coupon.code}' created.")
            return redirect("dashboard:coupon_list")
    else:
        form = CouponAdminForm()

    return render(request, "admin_dashboard/coupons/form.html", {"form": form, "title": "Create Coupon"})


@management_required
def coupon_edit(request, coupon_id):
    """Edit coupon."""
    coupon = get_object_or_404(Coupon, id=coupon_id)
    if request.method == "POST":
        form = CouponAdminForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, f"Coupon '{coupon.code}' updated.")
            return redirect("dashboard:coupon_list")
    else:
        form = CouponAdminForm(instance=coupon)

    return render(request, "admin_dashboard/coupons/form.html", {"form": form, "title": f"Edit Coupon {coupon.code}"})


@management_required
def coupon_delete(request, coupon_id):
    """Delete coupon."""
    coupon = get_object_or_404(Coupon, id=coupon_id)
    if request.method == "POST":
        coupon.delete()
        messages.success(request, f"Coupon '{coupon.code}' deleted.")
        return redirect("dashboard:coupon_list")

    return render(request, "admin_dashboard/coupons/confirm_delete.html", {"coupon": coupon})


# ==================== REVIEWS MODERATION ====================

@management_required
def review_list(request):
    """Moderate customer reviews."""
    reviews = ProductReview.objects.select_related("product", "user").order_by("-created_at")
    return render(request, "admin_dashboard/reviews/list.html", {"reviews": reviews})


@management_required
@require_POST
def review_toggle_approval(request, review_id):
    """Toggle review approval."""
    review = get_object_or_404(ProductReview, id=review_id)
    review.is_approved = not review.is_approved
    review.save()
    status_str = "Approved" if review.is_approved else "Hidden / Unapproved"
    messages.info(request, f"Review status changed to {status_str}.")
    return redirect("dashboard:review_list")


# ==================== BANNERS ====================

@management_required
def banner_list(request):
    """List marketing banners."""
    banners = Banner.objects.order_by("sort_order", "-created_at")
    return render(request, "admin_dashboard/banners/list.html", {"banners": banners})


@management_required
def banner_create(request):
    """Create marketing banner."""
    if request.method == "POST":
        form = BannerAdminForm(request.POST, request.FILES)
        if form.is_valid():
            banner = form.save()
            messages.success(request, f"Banner '{banner.title}' created.")
            return redirect("dashboard:banner_list")
    else:
        form = BannerAdminForm()

    return render(request, "admin_dashboard/banners/form.html", {"form": form, "title": "Create Banner"})


@management_required
def banner_edit(request, banner_id):
    """Edit marketing banner."""
    banner = get_object_or_404(Banner, id=banner_id)
    if request.method == "POST":
        form = BannerAdminForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            messages.success(request, f"Banner '{banner.title}' updated.")
            return redirect("dashboard:banner_list")
    else:
        form = BannerAdminForm(instance=banner)

    return render(request, "admin_dashboard/banners/form.html", {"form": form, "title": f"Edit {banner.title}"})


@management_required
def banner_delete(request, banner_id):
    """Delete marketing banner."""
    banner = get_object_or_404(Banner, id=banner_id)
    if request.method == "POST":
        banner.delete()
        messages.success(request, f"Banner '{banner.title}' deleted.")
        return redirect("dashboard:banner_list")

    return render(request, "admin_dashboard/banners/confirm_delete.html", {"banner": banner})


# ==================== CUSTOMERS ====================

@management_required
def customer_list(request):
    """List registered store customers."""
    customers = User.objects.filter(role=User.Role.CUSTOMER).annotate(order_count=Count("orders")).order_by("-date_joined")
    return render(request, "admin_dashboard/customers/list.html", {"customers": customers})


@management_required
def customer_detail(request, customer_id):
    """Customer profile, addresses, and order history."""
    customer = get_object_or_404(User.objects.prefetch_related("orders", "addresses"), id=customer_id)
    return render(request, "admin_dashboard/customers/detail.html", {"customer": customer})


# ==================== AUDIT LOGS ====================

@management_required
def audit_log_list(request):
    """Inspect system, security, and staff audit logs."""
    logs = AuditLog.objects.order_by("-timestamp")
    paginator = Paginator(logs, 25)
    page_obj = paginator.get_page(request.GET.get("page", 1))
    return render(request, "admin_dashboard/audit/list.html", {"page_obj": page_obj})


# ==================== STORE SETTINGS ====================

@management_required
def store_settings_view(request):
    """Configure store business parameters."""
    if request.method == "POST":
        for key, val in request.POST.items():
            if key.startswith("setting_"):
                real_key = key.replace("setting_", "")
                SiteSetting.objects.update_or_create(key=real_key, defaults={"value": val})
        messages.success(request, "Store settings saved successfully.")
        return redirect("dashboard:settings")

    settings_list = SiteSetting.objects.all()
    return render(request, "admin_dashboard/settings/settings.html", {"settings": settings_list})
