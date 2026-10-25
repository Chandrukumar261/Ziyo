from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.catalog.models import Category, Product
from apps.inventory.models import InventoryItem

User = get_user_model()

class CatalogCRUDTests(TestCase):
    """Tests for Product and Category CRUD operations and soft-delete invariants."""

    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_superuser(
            email="manager@ziyo.store",
            password="ManagerPassword123!",
            first_name="Staff",
        )
        self.client.force_login(self.staff_user)

        self.category = Category.objects.create(
            name="Living Accents",
            slug="living-accents",
            description="Minimal tactile decor objects",
        )

    def test_product_creation_and_inventory_link(self):
        """Staff can create a new product which auto-spawns an InventoryItem record."""
        response = self.client.post(reverse("dashboard:product_create"), {
            "name": "Sculptural Travertine Bookends",
            "category": str(self.category.id),
            "sku": "ZY-TRAV-999",
            "price": "2450.00",
            "compare_at_price": "2990.00",
            "cost_price": "1100.00",
            "short_description": "Hand-cut natural travertine stone bookends.",
            "description": "Solid honed travertine stone sculpted in organic arches.",
            "initial_stock": "30",
            "is_active": "on",
        })
        self.assertEqual(response.status_code, 302)
        product = Product.objects.get(sku="ZY-TRAV-999")
        self.assertEqual(product.price, Decimal("2450.00"))
        # Inventory verification
        inv = InventoryItem.objects.get(product=product)
        self.assertEqual(inv.quantity_on_hand, 30)
        self.assertEqual(inv.available_quantity, 30)

    def test_product_soft_deletion_archiving(self):
        """Deleting a product sets is_archived=True, retaining order consistency without raw deletion."""
        product = Product.objects.create(
            name="Archived Item",
            slug="archived-item",
            sku="ZY-ARCH-111",
            category=self.category,
            price=Decimal("1500.00"),
            is_active=True,
        )
        resp = self.client.post(reverse("dashboard:product_delete", kwargs={"product_id": product.id}))
        self.assertEqual(resp.status_code, 302)
        product.refresh_from_db()
        self.assertTrue(product.is_archived)
        self.assertFalse(product.is_active)
        # Should not appear in active storefront query
        self.assertNotIn(product, Product.active.all())
