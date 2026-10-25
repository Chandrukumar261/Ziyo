from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.catalog.models import Product, Category
from apps.inventory.models import InventoryItem, StockMovement
from apps.orders.models import Order, OrderItem, OrderStatusHistory, Shipment

User = get_user_model()


class CustomApiSuiteTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Regular customer
        self.customer = User.objects.create_user(
            email="shopper@ziyo.store",
            password="StrongPassword123!",
            first_name="Jane",
            last_name="Doe",
            role=User.Role.CUSTOMER,
        )

        # Staff user for ERP & admin APIs
        self.staff_user = User.objects.create_user(
            email="ops@ziyo.store",
            password="AdminPassword123!",
            first_name="Ops",
            last_name="Manager",
            role=User.Role.STORE_MANAGER,
            is_staff=True,
        )

        # Category and Product with Inventory
        self.category = Category.objects.create(name="Living", slug="living")
        self.product = Product.objects.create(
            category=self.category,
            name="Sculptural Ceramic Vase",
            slug="sculptural-ceramic-vase",
            sku="ZY-VASE-01",
            price=Decimal("1899.00"),
            is_active=True,
        )
        self.inventory = InventoryItem.objects.create(
            product=self.product,
            sku="ZY-VASE-01",
            quantity_on_hand=50,
            reserved_quantity=0,
        )

        # Test Order
        self.order = Order.objects.create(
            order_number=Order.generate_order_number(),
            user=self.customer,
            email=self.customer.email,
            phone="9876543210",
            status=Order.Status.PENDING,
            subtotal=Decimal("1899.00"),
            discount_amount=Decimal("0.00"),
            shipping_fee=Decimal("0.00"),
            tax_amount=Decimal("0.00"),
            total_amount=Decimal("1899.00"),
            shipping_full_name="Jane Doe",
            shipping_phone="9876543210",
            shipping_address_line_1="10 Downing Street",
            shipping_city="Mumbai",
            shipping_state="Maharashtra",
            shipping_postal_code="400001",
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name=self.product.name,
            sku=self.product.sku,
            unit_price=self.product.price,
            quantity=1,
            line_total=self.product.price,
        )
        OrderStatusHistory.objects.create(
            order=self.order,
            status=Order.Status.PENDING,
            notes="Order initiated by customer",
        )

    # 1. Test Interactive OpenAPI Schema & Swagger Documentation
    def test_openapi_schema_endpoint(self):
        resp = self.client.get("/api/v1/schema/")
        self.assertEqual(resp.status_code, 200)

    def test_swagger_ui_endpoint(self):
        resp = self.client.get("/api/v1/docs/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"swagger-ui", resp.content.lower())

    def test_redoc_ui_endpoint(self):
        resp = self.client.get("/api/v1/redoc/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"redoc", resp.content.lower())

    # 2. Test Customer Order History & Tracking
    def test_customer_order_history_requires_auth(self):
        resp = self.client.get("/api/v1/orders/")
        self.assertEqual(resp.status_code, 403)

    def test_customer_order_history_authenticated(self):
        self.client.force_login(self.customer)
        resp = self.client.get("/api/v1/orders/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["order_number"], self.order.order_number)

    def test_customer_order_detail_authenticated(self):
        self.client.force_login(self.customer)
        resp = self.client.get(f"/api/v1/orders/{self.order.order_number}/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["order"]["shipping_city"], "Mumbai")
        self.assertEqual(len(data["order"]["items"]), 1)

    def test_live_order_tracking_public(self):
        resp = self.client.get(f"/api/v1/orders/track/{self.order.order_number}/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["tracking"]["status"], Order.Status.PENDING)
        self.assertFalse(data["tracking"]["is_delivered"])
        self.assertTrue(len(data["tracking"]["timeline"]) >= 1)

    def test_update_shipping_address_allowed_before_dispatch(self):
        self.client.force_login(self.customer)
        payload = {
            "shipping_city": "Bengaluru",
            "shipping_postal_code": "560001",
            "shipping_address_line_1": "42 MG Road",
        }
        resp = self.client.patch(
            f"/api/v1/orders/{self.order.order_number}/shipping-address/",
            data=payload,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.shipping_city, "Bengaluru")
        self.assertEqual(self.order.shipping_postal_code, "560001")

    def test_update_shipping_address_rejected_after_dispatch(self):
        self.order.status = Order.Status.SHIPPED
        self.order.save()

        self.client.force_login(self.customer)
        payload = {"shipping_city": "Chennai"}
        resp = self.client.patch(
            f"/api/v1/orders/{self.order.order_number}/shipping-address/",
            data=payload,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Shipping address cannot be modified", resp.json()["error"])

    # 3. Test External ERP & Logistics Webhook API
    def test_erp_bulk_inventory_sync_requires_staff(self):
        payload = {
            "batch_id": "BATCH-001",
            "items": [{"sku": "ZY-VASE-01", "quantity_on_hand": 120}],
        }
        resp = self.client.post("/api/v1/erp/inventory/bulk-sync/", data=payload, content_type="application/json")
        self.assertEqual(resp.status_code, 403)

    def test_erp_bulk_inventory_sync_staff_success(self):
        self.client.force_login(self.staff_user)
        payload = {
            "batch_id": "BATCH-2026-X",
            "items": [{"sku": "ZY-VASE-01", "quantity_on_hand": 85}],
        }
        resp = self.client.post("/api/v1/erp/inventory/bulk-sync/", data=payload, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["processed_count"], 1)

        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity_on_hand, 85)

        # Ledger stock movement recorded
        movement = StockMovement.objects.filter(inventory_item=self.inventory, reference_id="ERP-BATCH-2026-X").first()
        self.assertIsNotNone(movement)
        self.assertEqual(movement.quantity, 35)  # 85 - 50 = +35

    def test_3pl_logistics_dispatch_webhook(self):
        self.client.force_login(self.staff_user)
        payload = {
            "order_number": self.order.order_number,
            "carrier": "BlueDart Express",
            "tracking_number": "BD-9876543210-IN",
            "estimated_delivery": "2026-10-30",
            "dispatch_notes": "Picked up from Central Fulfillment Hub",
        }
        resp = self.client.post("/api/v1/erp/logistics/dispatch/", data=payload, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["status"], Order.Status.SHIPPED)

        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.SHIPPED)
        self.assertEqual(self.order.carrier, "BlueDart Express")
        self.assertEqual(self.order.tracking_number, "BD-9876543210-IN")

        # Shipment model exists
        shipment = Shipment.objects.filter(order=self.order).first()
        self.assertIsNotNone(shipment)
        self.assertEqual(shipment.carrier, "BlueDart Express")

    def test_erp_generic_webhook_listener(self):
        payload = {
            "event_type": "warehouse.stock.cycle_count",
            "event_id": "EVT-88992",
            "data": {"warehouse_id": "WH-WEST", "accuracy_score": 0.998},
        }
        resp = self.client.post("/api/v1/erp/webhooks/listener/", data=payload, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["status"], "acknowledged")
