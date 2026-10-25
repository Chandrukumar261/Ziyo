from decimal import Decimal
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.catalog.models import Category, Product
from apps.inventory.models import InventoryItem
from apps.orders.models import Order
from apps.payments.razorpay_service import RazorpayService

User = get_user_model()

class CustomAPISecurityAndHardeningTests(TestCase):
    """
    Automated security tests for:
    1. Server-side payment security & authoritative order creation.
    2. Server-side price authority and inventory validation.
    3. Server-side RBAC authorization on Custom REST APIs.
    4. HTTP Security Headers (CSP, nosniff, frame-ancestors, etc.).
    """

    def setUp(self):
        self.client = Client()
        self.customer = User.objects.create_user(
            email="api_buyer@ziyo.store",
            password="SecurePassword123!",
            role=User.Role.CUSTOMER,
        )
        self.staff_user = User.objects.create_user(
            email="api_staff@ziyo.store",
            password="SecurePassword123!",
            role=User.Role.STAFF,
            is_staff=True,
        )

        self.category = Category.objects.create(name="Living", slug="living")
        self.product = Product.objects.create(
            name="Hand-Thrown Terracotta Urn",
            slug="terracotta-urn",
            sku="URN-001",
            category=self.category,
            price=Decimal("2500.00"),
            is_active=True,
        )
        self.inventory = InventoryItem.objects.create(
            product=self.product,
            sku=self.product.sku,
            quantity_on_hand=10,
            reserved_quantity=0,
            low_stock_threshold=2,
        )

    def test_security_headers_present_on_response(self):
        """Security headers middleware adds CSP, nosniff, frame denial, and referrer policy."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        # 1. Content-Security-Policy
        self.assertIn("Content-Security-Policy", response.headers)
        csp = response.headers["Content-Security-Policy"]
        self.assertIn("default-src 'self'", csp)
        self.assertIn("frame-ancestors 'none'", csp)

        # 2. X-Content-Type-Options
        self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")

        # 3. X-Frame-Options
        self.assertEqual(response.headers.get("X-Frame-Options"), "DENY")

        # 4. Referrer-Policy
        self.assertEqual(response.headers.get("Referrer-Policy"), "strict-origin-when-cross-origin")

        # 5. Permissions-Policy
        self.assertIn("Permissions-Policy", response.headers)

    def test_cart_and_checkout_api_enforces_server_side_price_authority(self):
        """
        Checkout API enforces server-side price authority:
        Prices are calculated strictly from database records, not from client payload.
        """
        self.client.force_login(self.customer)

        # Add item to cart via API
        add_resp = self.client.post(
            reverse("api_v1:cart_add_item"),
            data=json.dumps({"product_id": str(self.product.id), "quantity": 2}),
            content_type="application/json",
        )
        self.assertEqual(add_resp.status_code, 201)

        # Checkout with address details
        checkout_resp = self.client.post(
            reverse("api_v1:checkout_order_create"),
            data=json.dumps({
                "full_name": "API Tester",
                "email": "api_buyer@ziyo.store",
                "phone": "+91 99999 88888",
                "address_line_1": "123 Sanctuary Way",
                "city": "Bengaluru",
                "state": "Karnataka",
                "postal_code": "560001",
            }),
            content_type="application/json",
        )
        self.assertEqual(checkout_resp.status_code, 201)
        data = checkout_resp.json()

        self.assertIn("order_number", data)
        self.assertIn("razorpay_order_id", data)

        # Verify Order in DB has authoritative price: 2 * 2500 = 5000 + tax - discount
        order = Order.objects.get(order_number=data["order_number"])
        self.assertEqual(order.subtotal, Decimal("5000.00"))
        self.assertEqual(order.status, Order.Status.PAYMENT_PENDING)

        # Verify stock was reserved
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.reserved_quantity, 2)
        self.assertEqual(self.inventory.available_quantity, 8)

    def test_payment_verify_api_rejects_invalid_tampered_signature(self):
        """Payment verification rejects counterfeit/tampered HMAC signatures with 400 Bad Request."""
        order = Order.objects.create(
            order_number="ZY-TAMPER-TEST",
            user=self.customer,
            email=self.customer.email,
            phone="1234567890",
            status=Order.Status.PAYMENT_PENDING,
            subtotal=Decimal("2500.00"),
            total_amount=Decimal("2500.00"),
            shipping_full_name="Tester",
            shipping_address_line_1="Addr",
            shipping_city="City",
            shipping_state="State",
            shipping_postal_code="560001",
        )

        resp = self.client.post(
            reverse("api_v1:payment_verify"),
            data=json.dumps({
                "order_number": order.order_number,
                "razorpay_order_id": "order_fake123",
                "razorpay_payment_id": "pay_fake123",
                "razorpay_signature": "counterfeit_tampered_signature_hex",
            }),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("verification failed", resp.json()["error"])

        # Order must remain unverified
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.PAYMENT_PENDING)

    def test_payment_verify_api_accepts_valid_signature_and_finalizes_order(self):
        """Payment verification validates legitimate signature, transitions to PAID, and commits inventory."""
        order = Order.objects.create(
            order_number="ZY-VALID-PAY-TEST",
            user=self.customer,
            email=self.customer.email,
            phone="1234567890",
            status=Order.Status.PAYMENT_PENDING,
            subtotal=Decimal("2500.00"),
            total_amount=Decimal("2500.00"),
            shipping_full_name="Tester",
            shipping_address_line_1="Addr",
            shipping_city="City",
            shipping_state="State",
            shipping_postal_code="560001",
        )
        self.inventory.reserve_stock(quantity=1, reference_id=order.order_number)

        # In dev/test mode sandbox_sig_ is verified
        resp = self.client.post(
            reverse("api_v1:payment_verify"),
            data=json.dumps({
                "order_number": order.order_number,
                "razorpay_order_id": "order_test_valid_123",
                "razorpay_payment_id": "pay_test_valid_123",
                "razorpay_signature": "sandbox_sig_order_test_valid_123_pay_test_valid_123",
            }),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["success"])

        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.PAID)

    def test_admin_api_rbac_authorization_denies_ordinary_customer(self):
        """
        RBAC security: Ordinary customer accounts are denied access to /api/v1/admin/ APIs
        with HTTP 403 Forbidden.
        """
        self.client.force_login(self.customer)

        # Customer attempts to list admin products
        resp = self.client.get(reverse("api_v1:admin_products"))
        self.assertEqual(resp.status_code, 403)

        # Customer attempts to adjust inventory
        adjust_resp = self.client.post(
            reverse("api_v1:admin_inventory_adjust"),
            data=json.dumps({"sku": self.product.sku, "quantity_change": 50, "movement_type": "RESTOCK"}),
            content_type="application/json",
        )
        self.assertEqual(adjust_resp.status_code, 403)

    def test_admin_api_rbac_authorization_permits_staff_member(self):
        """RBAC security: Authenticated staff members are permitted access to /api/v1/admin/ APIs."""
        self.client.force_login(self.staff_user)

        # Staff lists admin products
        resp = self.client.get(reverse("api_v1:admin_products"))
        self.assertEqual(resp.status_code, 200)

        # Staff adjusts inventory
        adjust_resp = self.client.post(
            reverse("api_v1:admin_inventory_adjust"),
            data=json.dumps({
                "sku": self.product.sku,
                "quantity_change": 15,
                "movement_type": "PURCHASE_RECEIPT",
                "notes": "Warehouse pallet received",
            }),
            content_type="application/json",
        )
        self.assertEqual(adjust_resp.status_code, 200)

        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity_on_hand, 25)
