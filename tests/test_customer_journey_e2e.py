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
from apps.payments.models import Payment

User = get_user_model()

class CompleteE2EJourneyTests(TestCase):
    """
    End-to-end integration test simulating complete customer and administrator journeys.
    Customer: Register -> Browse -> Add to Cart -> Apply Coupon -> Checkout -> Pay -> Confirm.
    Admin: Login -> Inspect Order -> Fulfill with Carrier Tracking.
    """

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Ceramics", slug="ceramics", is_active=True)
        self.product = Product.objects.create(
            name="Handmade Ceramic Mug",
            slug="handmade-ceramic-mug",
            sku="ZY-MUG-01",
            category=self.category,
            price=Decimal("800.00"),
            is_active=True,
        )
        self.inventory = InventoryItem.objects.create(
            product=self.product,
            sku=self.product.sku,
            quantity_on_hand=20,
        )

        now = timezone.now()
        self.coupon = Coupon.objects.create(
            code="WELCOME10",
            discount_type=Coupon.DiscountType.PERCENTAGE,
            value=Decimal("10.00"),
            min_purchase_amount=Decimal("500.00"),
            valid_from=now,
            valid_to=now + datetime.timedelta(days=30),
            is_active=True,
        )

        self.staff_admin = User.objects.create_superuser(
            email="ziyo@example.com",
            password="ziyo",
            role=User.Role.SUPERUSER,
        )

    def test_full_customer_and_admin_lifecycle(self):
        # 1. Customer Registration
        reg_resp = self.client.post(reverse("accounts:register"), {
            "email": "priya@example.com",
            "first_name": "Priya",
            "last_name": "Nair",
            "phone": "+919876500000",
            "password": "CustomerSecurePass123!",
            "confirm_password": "CustomerSecurePass123!",
        })
        self.assertEqual(reg_resp.status_code, 302)
        customer = User.objects.get(email="priya@example.com")

        # 2. Browse Product Detail
        detail_resp = self.client.get(reverse("catalog:product_detail", kwargs={"slug": self.product.slug}))
        self.assertEqual(detail_resp.status_code, 200)

        # 3. Add to Cart (2 units = 1600.00)
        add_resp = self.client.post(reverse("cart:add_to_cart", kwargs={"product_id": self.product.id}), {
            "quantity": 2,
        })
        self.assertEqual(add_resp.status_code, 302)

        # 4. Apply Coupon
        coupon_resp = self.client.post(reverse("discounts:apply_coupon"), {"code": "WELCOME10"})
        self.assertEqual(coupon_resp.status_code, 302)

        # 5. Checkout
        checkout_resp = self.client.post(reverse("checkout:checkout_process"), {
            "email": customer.email,
            "phone": customer.phone,
            "full_name": customer.full_name,
            "address_line_1": "14 Lotus Boulevard",
            "city": "Mumbai",
            "state": "Maharashtra",
            "postal_code": "400001",
            "customer_notes": "Handle ceramics with care",
        })
        self.assertEqual(checkout_resp.status_code, 302)

        order = Order.objects.filter(user=customer).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.status, Order.Status.PAYMENT_PENDING)

        # 6. Simulate Sandbox Payment Verification
        pay_resp = self.client.post(reverse("payments:callback"), {
            "order_number": order.order_number,
            "razorpay_order_id": "order_sandbox_123",
            "razorpay_payment_id": "pay_sandbox_999",
            "razorpay_signature": f"sandbox_sig_{order.order_number}",
        })
        self.assertEqual(pay_resp.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.PAID)

        # Verify inventory sold: 20 - 2 = 18
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity_on_hand, 18)

        # 7. Customer views order confirmation
        success_resp = self.client.get(reverse("orders:order_success", kwargs={"order_number": order.order_number}))
        self.assertEqual(success_resp.status_code, 200)

        # 8. Admin fulfillment at /management/
        admin_client = Client()
        admin_client.force_login(self.staff_admin)

        fulfill_resp = admin_client.post(reverse("dashboard:order_detail", kwargs={"order_id": order.id}), {
            "status": Order.Status.SHIPPED,
            "carrier": "Blue Dart Express",
            "tracking_number": "BLUEDART-8839210",
            "admin_notes": "Dispatched via air cargo with bubble wrap.",
        })
        self.assertEqual(fulfill_resp.status_code, 302)

        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.SHIPPED)
        self.assertEqual(order.tracking_number, "BLUEDART-8839210")
