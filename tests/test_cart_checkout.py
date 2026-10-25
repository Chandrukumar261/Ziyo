import datetime
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.catalog.models import Category, Product
from apps.inventory.models import InventoryItem
from apps.discounts.models import Coupon
from apps.orders.models import Order
from apps.cart.cart_service import get_or_create_cart, calculate_cart_totals

User = get_user_model()

class CartAndCheckoutTests(TestCase):
    """Tests shopping cart calculations, coupons, and transactional checkout."""

    def setUp(self):
        self.client = Client()
        self.customer = User.objects.create_user(
            email="shopper@ziyo.store",
            password="ShopperPassword123!",
            first_name="Ananya",
        )
        self.client.force_login(self.customer)

        self.category = Category.objects.create(name="Linens", slug="linens")
        self.product = Product.objects.create(
            name="Organic Linen Pillowcase Set",
            slug="organic-linen-pillowcase-set",
            sku="ZY-LIN-001",
            category=self.category,
            price=Decimal("1200.00"),
            is_active=True,
        )
        self.inventory = InventoryItem.objects.create(
            product=self.product,
            sku=self.product.sku,
            quantity_on_hand=50,
        )

        now = timezone.now()
        self.coupon = Coupon.objects.create(
            code="SAVE10",
            discount_type=Coupon.DiscountType.PERCENTAGE,
            value=Decimal("10.00"),
            min_purchase_amount=Decimal("1000.00"),
            valid_from=now,
            valid_to=now + datetime.timedelta(days=30),
            is_active=True,
        )

    def test_add_to_cart_and_totals_calculation(self):
        """Tests adding product to cart and verifying server-side price computation."""
        # Add 2 items
        resp = self.client.post(reverse("cart:add_to_cart", kwargs={"product_id": self.product.id}), {
            "quantity": 2,
        })
        self.assertEqual(resp.status_code, 302)

        # Apply Coupon
        coupon_resp = self.client.post(reverse("discounts:apply_coupon"), {"code": "SAVE10"})
        self.assertEqual(coupon_resp.status_code, 302)

        # Inspect cart calculation
        cart = get_or_create_cart(coupon_resp.wsgi_request)
        totals = calculate_cart_totals(cart, coupon_resp.wsgi_request)

        # 2 x 1200 = 2400 subtotal
        self.assertEqual(totals["subtotal"], Decimal("2400.00"))
        # 10% discount on 2400 = 240
        self.assertEqual(totals["discount_amount"], Decimal("240.00"))
        # 2400 is above free shipping threshold (1499) -> shipping = 0
        self.assertEqual(totals["shipping_fee"], Decimal("0.00"))
        # Taxable amount = 2400 - 240 = 2160. 5% GST = 108.00
        self.assertEqual(totals["tax_amount"], Decimal("108.00"))
        # Grand total = 2160 + 0 + 108 = 2268.00
        self.assertEqual(totals["total"], Decimal("2268.00"))

    def test_checkout_creates_order_and_reserves_inventory(self):
        """Checkout transactionally creates an Order record and places an inventory hold."""
        # Add 1 item
        self.client.post(reverse("cart:add_to_cart", kwargs={"product_id": self.product.id}), {"quantity": 2})

        checkout_resp = self.client.post(reverse("checkout:checkout_process"), {
            "email": "shopper@ziyo.store",
            "phone": "+919876543210",
            "full_name": "Ananya Sharma",
            "country": "IN",
            "address_line_1": "Flat 402, Lotus Enclave",
            "address_line_2": "MG Road",
            "city": "Bengaluru",
            "state": "Karnataka",
            "postal_code": "560001",
            "payment_method": "RAZORPAY_CARD",
            "customer_notes": "Leave at front desk",
        })
        # Should redirect to payment gateway
        self.assertEqual(checkout_resp.status_code, 302)
        self.assertIn("payments/pay/", checkout_resp.url)
        order = Order.objects.filter(email="shopper@ziyo.store").first()
        self.assertIsNotNone(order)
        self.assertEqual(order.status, Order.Status.PAYMENT_PENDING)
        self.assertEqual(order.shipping_city, "Bengaluru")
        self.assertEqual(order.shipping_country, "India")

        # Verify inventory reservation
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.reserved_quantity, 2)
        self.assertEqual(self.inventory.available_quantity, 48)

    def test_checkout_with_cash_on_delivery(self):
        """Cash on Delivery creates confirmed processing order and commits inventory."""
        self.client.post(reverse("cart:add_to_cart", kwargs={"product_id": self.product.id}), {"quantity": 1})

        checkout_resp = self.client.post(reverse("checkout:checkout_process"), {
            "email": "cod_shopper@ziyo.store",
            "phone": "+919876543210",
            "full_name": "Rohan Verma",
            "country": "IN",
            "address_line_1": "House 12, Indiranagar",
            "city": "Bengaluru",
            "state": "Karnataka",
            "postal_code": "560038",
            "payment_method": "COD",
        })
        # Should redirect directly to order success
        self.assertEqual(checkout_resp.status_code, 302)
        self.assertIn("/success/", checkout_resp.url)

        order = Order.objects.filter(email="cod_shopper@ziyo.store").first()
        self.assertIsNotNone(order)
        self.assertEqual(order.status, Order.Status.PROCESSING)
        self.assertEqual(order.payment.provider, "COD")
        self.assertEqual(order.payment.payment_method_type, "CASH_ON_DELIVERY")

    def test_checkout_with_international_country_and_postal_code(self):
        """Tests checkout with global countries and international postal codes."""
        self.client.post(reverse("cart:add_to_cart", kwargs={"product_id": self.product.id}), {"quantity": 1})

        checkout_resp = self.client.post(reverse("checkout:checkout_process"), {
            "email": "us_shopper@ziyo.store",
            "phone": "+14155552671",
            "full_name": "Alexander Hayes",
            "country": "US",
            "address_line_1": "742 Evergreen Terrace",
            "city": "Springfield",
            "state": "Oregon",
            "postal_code": "97477",
            "payment_method": "RAZORPAY_CARD",
        })
        self.assertEqual(checkout_resp.status_code, 302)
        order = Order.objects.filter(email="us_shopper@ziyo.store").first()
        self.assertIsNotNone(order)
        self.assertEqual(order.shipping_country, "United States")
        self.assertEqual(order.shipping_postal_code, "97477")

    def test_checkout_rejects_invalid_indian_pin_code(self):
        """Invalid 5-digit or alpha Indian PIN is rejected by server."""
        self.client.post(reverse("cart:add_to_cart", kwargs={"product_id": self.product.id}), {"quantity": 1})

        checkout_resp = self.client.post(reverse("checkout:checkout_process"), {
            "email": "shopper@ziyo.store",
            "phone": "+919876543210",
            "full_name": "Ananya Sharma",
            "country": "IN",
            "address_line_1": "Flat 402, Lotus Enclave",
            "city": "Bengaluru",
            "state": "Karnataka",
            "postal_code": "1234",  # Invalid PIN
            "payment_method": "RAZORPAY_CARD",
        })
        # Should stay on checkout page with validation error
        self.assertEqual(checkout_resp.status_code, 200)
        self.assertFormError(checkout_resp.context["form"], "postal_code", "Please enter a valid 6-digit Indian PIN code (e.g. 560001, 110001).")
