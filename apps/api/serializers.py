from decimal import Decimal
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from apps.catalog.models import Product, Category, ProductVariant, ProductImage
from apps.inventory.models import InventoryItem, StockMovement
from apps.orders.models import Order, OrderItem, OrderStatusHistory, Shipment
from apps.payments.models import Payment
from apps.cart.models import Cart, CartItem

User = get_user_model()

# ==================== PRODUCT & CATALOG SERIALIZERS ====================
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "alt_text", "is_primary", "sort_order")


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ("id", "name", "sku", "price_adjustment", "final_price", "is_active")


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    available_stock = serializers.IntegerField(source="inventory.available_quantity", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "sku",
            "category",
            "category_name",
            "description",
            "price",
            "compare_at_price",
            "is_active",
            "is_featured",
            "is_trending",
            "available_stock",
            "images",
            "variants",
        )


# ==================== CART SERIALIZERS ====================
class CartItemInputSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    variant_id = serializers.UUIDField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1, default=1)


class CartItemResponseSerializer(serializers.Serializer):
    item_id = serializers.UUIDField()
    product_id = serializers.UUIDField()
    product_name = serializers.CharField()
    variant_name = serializers.CharField(allow_blank=True)
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    quantity = serializers.IntegerField()
    line_total = serializers.DecimalField(max_digits=12, decimal_places=2)
    image_url = serializers.CharField()


class CartTotalsResponseSerializer(serializers.Serializer):
    items = CartItemResponseSerializer(many=True)
    total_items = serializers.IntegerField()
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    coupon_code = serializers.CharField(allow_blank=True)
    shipping_fee = serializers.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    total = serializers.DecimalField(max_digits=12, decimal_places=2)


# ==================== CHECKOUT & ORDER CREATION SERIALIZERS ====================
class CheckoutOrderCreateSerializer(serializers.Serializer):
    """
    Validates shipping and contact parameters.
    Prices are strictly ignored from client and computed from database records only.
    """
    full_name = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=100, required=False, default="India")
    address_line_1 = serializers.CharField(max_length=255)
    address_line_2 = serializers.CharField(max_length=255, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20)
    payment_method = serializers.ChoiceField(
        choices=["RAZORPAY_CARD", "RAZORPAY_UPI", "COD"],
        required=False,
        default="RAZORPAY_CARD",
    )
    customer_notes = serializers.CharField(required=False, allow_blank=True)
    coupon_code = serializers.CharField(required=False, allow_blank=True)


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "order_number",
            "status",
            "subtotal",
            "discount_amount",
            "coupon_code",
            "shipping_fee",
            "tax_amount",
            "total_amount",
            "shipping_full_name",
            "shipping_city",
            "shipping_state",
            "shipping_postal_code",
            "created_at",
        )


# ==================== PAYMENT VERIFICATION SERIALIZERS ====================
class PaymentVerificationSerializer(serializers.Serializer):
    """
    Cryptographic verification payload for Razorpay HMAC verification.
    """
    order_number = serializers.CharField()
    razorpay_order_id = serializers.CharField()
    razorpay_payment_id = serializers.CharField()
    razorpay_signature = serializers.CharField()


# ==================== AUTHENTICATION SERIALIZERS ====================
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "phone", "password")

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data, role=User.Role.CUSTOMER)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email", "").lower().strip()
        password = attrs.get("password")
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("Account is disabled.")
        attrs["user"] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "phone", "role", "is_staff")
        read_only_fields = ("id", "email", "role", "is_staff")


# ==================== ADMIN & INVENTORY SERIALIZERS ====================
class InventoryAdjustSerializer(serializers.Serializer):
    sku = serializers.CharField()
    quantity_change = serializers.IntegerField()
    movement_type = serializers.ChoiceField(choices=StockMovement.MovementType.choices)
    notes = serializers.CharField(required=False, allow_blank=True)


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.Status.choices)
    notes = serializers.CharField(required=False, allow_blank=True)
    tracking_number = serializers.CharField(required=False, allow_blank=True)


# ==================== CUSTOMER ORDER & TRACKING SERIALIZERS ====================
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product_name",
            "variant_name",
            "sku",
            "unit_price",
            "quantity",
            "line_total",
        )


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ("id", "status", "notes", "created_at")


class CustomerOrderListSerializer(serializers.ModelSerializer):
    items_count = serializers.IntegerField(source="items.count", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "order_number",
            "status",
            "total_amount",
            "items_count",
            "tracking_number",
            "carrier",
            "created_at",
        )


class CustomerOrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "order_number",
            "status",
            "subtotal",
            "discount_amount",
            "coupon_code",
            "shipping_fee",
            "tax_amount",
            "total_amount",
            "shipping_full_name",
            "shipping_phone",
            "shipping_address_line_1",
            "shipping_address_line_2",
            "shipping_city",
            "shipping_state",
            "shipping_postal_code",
            "shipping_country",
            "customer_notes",
            "tracking_number",
            "carrier",
            "created_at",
            "items",
            "status_history",
        )


class OrderLiveTrackingSerializer(serializers.Serializer):
    order_number = serializers.CharField()
    status = serializers.CharField()
    carrier = serializers.CharField(allow_blank=True)
    tracking_number = serializers.CharField(allow_blank=True)
    shipped_at = serializers.DateTimeField(allow_null=True)
    estimated_delivery = serializers.DateField(allow_null=True)
    is_delivered = serializers.BooleanField()
    timeline = OrderStatusHistorySerializer(many=True)


class OrderShippingAddressUpdateSerializer(serializers.Serializer):
    shipping_full_name = serializers.CharField(max_length=150, required=False)
    shipping_phone = serializers.CharField(max_length=20, required=False)
    shipping_address_line_1 = serializers.CharField(max_length=255, required=False)
    shipping_address_line_2 = serializers.CharField(max_length=255, required=False, allow_blank=True)
    shipping_city = serializers.CharField(max_length=100, required=False)
    shipping_state = serializers.CharField(max_length=100, required=False)
    shipping_postal_code = serializers.CharField(max_length=20, required=False)
    customer_notes = serializers.CharField(required=False, allow_blank=True)


# ==================== ERP & LOGISTICS WEBHOOK SERIALIZERS ====================
class ErpInventoryItemSyncSerializer(serializers.Serializer):
    sku = serializers.CharField(max_length=80)
    quantity_on_hand = serializers.IntegerField(min_value=0)
    warehouse_code = serializers.CharField(max_length=50, required=False, default="MAIN")


class ErpBulkInventorySyncSerializer(serializers.Serializer):
    batch_id = serializers.CharField(max_length=100)
    source = serializers.CharField(max_length=100, required=False, default="ERP_SYNC")
    items = ErpInventoryItemSyncSerializer(many=True)


class LogisticsDispatchSerializer(serializers.Serializer):
    order_number = serializers.CharField(max_length=40)
    carrier = serializers.CharField(max_length=100)
    tracking_number = serializers.CharField(max_length=120)
    estimated_delivery = serializers.DateField(required=False, allow_null=True)
    dispatch_notes = serializers.CharField(required=False, allow_blank=True)


class ErpGenericWebhookSerializer(serializers.Serializer):
    event_type = serializers.CharField(max_length=100)
    event_id = serializers.CharField(max_length=100, required=False)
    timestamp = serializers.DateTimeField(required=False)
    data = serializers.DictField()
