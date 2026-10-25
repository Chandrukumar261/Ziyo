import json
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.catalog.models import Category, Product
from apps.inventory.models import InventoryItem
from apps.orders.models import Order, OrderItem
from apps.payments.models import Payment, PaymentWebhookEvent
from apps.payments.razorpay_service import RazorpayService

User = get_user_model()

class PaymentAndWebhookTests(TestCase):
    """Tests payment verification, signature tampering rejection, and duplicate webhook protection."""

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Candles", slug="candles")
        self.product = Product.objects.create(
            name="Amber Candle",
            slug="amber-candle",
            sku="ZY-CND-1",
            category=self.category,
            price=Decimal("900.00"),
            is_active=True,
        )
        self.inventory = InventoryItem.objects.create(
            product=self.product,
            sku=self.product.sku,
            quantity_on_hand=30,
            reserved_quantity=2,
        )
        self.order = Order.objects.create(
            order_number="ZY-TEST-001",
            email="testpay@ziyo.store",
            phone="+919999999999",
            status=Order.Status.PAYMENT_PENDING,
            subtotal=Decimal("1800.00"),
            discount_amount=Decimal("0.00"),
            shipping_fee=Decimal("0.00"),
            tax_amount=Decimal("90.00"),
            total_amount=Decimal("1890.00"),
            shipping_full_name="Test Customer",
            shipping_address_line_1="10 Downing",
            shipping_city="Delhi",
            shipping_state="Delhi",
            shipping_postal_code="110001",
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name=self.product.name,
            sku=self.product.sku,
            unit_price=Decimal("900.00"),
            quantity=2,
            line_total=Decimal("1800.00"),
        )

    def test_payment_callback_valid_signature_settles_order_and_inventory(self):
        """Valid sandbox payment signature marks order as PAID and commits inventory deduction."""
        response = self.client.post(reverse("payments:callback"), {
            "order_number": self.order.order_number,
            "razorpay_order_id": "order_test_12345",
            "razorpay_payment_id": "pay_test_99999",
            "razorpay_signature": f"sandbox_sig_{self.order.order_number}",
        })
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.PAID)

        # Inventory committed: on_hand deducted from 30 to 28, reserved cleared
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity_on_hand, 28)
        self.assertEqual(self.inventory.reserved_quantity, 0)

        # Payment record created
        payment = Payment.objects.get(order=self.order)
        self.assertEqual(payment.status, Payment.Status.CAPTURED)
        self.assertEqual(payment.amount, Decimal("1890.00"))

    def test_payment_callback_invalid_tampered_signature_rejected(self):
        """Tampered cryptographic signature is rejected, and order remains unpaid."""
        response = self.client.post(reverse("payments:callback"), {
            "order_number": self.order.order_number,
            "razorpay_order_id": "order_test_12345",
            "razorpay_payment_id": "pay_test_99999",
            "razorpay_signature": "MALICIOUS_TAMPERED_SIGNATURE",
        })
        # Should redirect to failure page
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertNotEqual(self.order.status, Order.Status.PAID)
        self.assertFalse(Payment.objects.filter(order=self.order).exists())

    def test_duplicate_webhook_protection_is_idempotent(self):
        """Re-delivery of the exact same webhook event ID does not duplicate records or financial calls."""
        event_id = "evt_duplicate_test_12345"
        payload = {
            "event_id": event_id,
            "event": "payment.captured",
            "payload": {
                "payment": {
                    "entity": {
                        "id": "pay_webhook_99",
                        "order_id": "order_123",
                        "notes": {"order_number": self.order.order_number},
                        "method": "UPI",
                    }
                }
            }
        }
        body = json.dumps(payload)
        service = RazorpayService()
        import hmac, hashlib
        sig = hmac.new(service.webhook_secret.encode(), body.encode(), hashlib.sha256).hexdigest()

        # First delivery
        resp1 = self.client.post(
            reverse("payments:razorpay_webhook"),
            data=body,
            content_type="application/json",
            HTTP_X_RAZORPAY_SIGNATURE=sig,
        )
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(PaymentWebhookEvent.objects.filter(event_id=event_id).count(), 1)

        # Second delivery (replay)
        resp2 = self.client.post(
            reverse("payments:razorpay_webhook"),
            data=body,
            content_type="application/json",
            HTTP_X_RAZORPAY_SIGNATURE=sig,
        )
        self.assertEqual(resp2.status_code, 200)
        # Verify still exactly 1 event record
        self.assertEqual(PaymentWebhookEvent.objects.filter(event_id=event_id).count(), 1)

    def test_switch_to_cod_from_payment_page(self):
        """Customer on payment gateway can switch method to Cash on Delivery."""
        resp = self.client.post(reverse("payments:switch_to_cod", kwargs={"order_number": self.order.order_number}))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/success/", resp.url)

        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.PROCESSING)
        payment = Payment.objects.filter(order=self.order).first()
        self.assertIsNotNone(payment)
        self.assertEqual(payment.provider, "COD")
        self.assertEqual(payment.payment_method_type, "CASH_ON_DELIVERY")
