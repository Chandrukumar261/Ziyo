"""
Tests for Dual-Portal Isolation Architecture:
1. Customer Storefront (Port 8000): Management portal is completely hidden & returns 404.
2. Management Portal (Port 8001): Dedicated administrative interface, customer cart/checkout returns 404.
"""

from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model

User = get_user_model()

class PortalIsolationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            email="staff_isolated@ziyo.store",
            password="Password123!",
            role=User.Role.STAFF,
            is_staff=True,
        )

    @override_settings(ROOT_URLCONF="config.urls_storefront")
    def test_storefront_portal_completely_hides_management(self):
        """
        On the customer storefront website (Port 8000):
        1. Storefront home and catalog are accessible.
        2. /management/ and /django-admin/ return 404 (completely hidden).
        3. Storefront HTML has no management dashboard button.
        """
        # Storefront home is active
        home_resp = self.client.get("/")
        self.assertEqual(home_resp.status_code, 200)
        self.assertNotContains(home_resp, "Management Dashboard")
        self.assertNotContains(home_resp, "/management/")

        # Management and django-admin URLs are completely absent (404)
        mgmt_resp = self.client.get("/management/")
        self.assertEqual(mgmt_resp.status_code, 404)

        admin_resp = self.client.get("/django-admin/")
        self.assertEqual(admin_resp.status_code, 404)

    @override_settings(ROOT_URLCONF="config.urls_management")
    def test_management_portal_serves_admin_at_root_and_hides_storefront_checkout(self):
        """
        On the dedicated management portal website (Port 8001):
        1. Root / routes to administrative overview.
        2. Authenticated staff can access management features.
        3. Storefront shopping cart & checkout are disabled (404).
        """
        self.client.force_login(self.staff_user)

        # Root / serves dashboard overview
        mgmt_root = self.client.get("/")
        self.assertEqual(mgmt_root.status_code, 200)
        self.assertContains(mgmt_root, "Executive Dashboard")

        # Management products list is active
        products_resp = self.client.get("/products/")
        self.assertEqual(products_resp.status_code, 200)

        # Storefront cart & checkout routes do not exist on management portal
        cart_resp = self.client.get("/cart/")
        self.assertEqual(cart_resp.status_code, 404)

        checkout_resp = self.client.get("/checkout/")
        self.assertEqual(checkout_resp.status_code, 404)
