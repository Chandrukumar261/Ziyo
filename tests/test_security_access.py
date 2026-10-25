from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.orders.models import Order

User = get_user_model()

class SecurityAndAuthorizationTests(TestCase):
    """Tests defense-in-depth security, role authorization, and data isolation."""

    def setUp(self):
        self.client = Client()
        self.customer1 = User.objects.create_user(
            email="cust1@ziyo.store",
            password="Password123!",
            role=User.Role.CUSTOMER,
        )
        self.customer2 = User.objects.create_user(
            email="cust2@ziyo.store",
            password="Password123!",
            role=User.Role.CUSTOMER,
        )
        self.staff_user = User.objects.create_user(
            email="staff@ziyo.store",
            password="Password123!",
            role=User.Role.STAFF,
            is_staff=True,
        )

    def test_anonymous_guest_management_access_redirects_to_staff_login(self):
        """Unauthenticated guest attempting to access /management/ is redirected to staff login."""
        response = self.client.get(reverse("dashboard:overview"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/management/login/", response.url)

    def test_ordinary_customer_management_access_raises_403_forbidden(self):
        """Authenticated ordinary customer attempting to access /management/ is denied with 403."""
        self.client.force_login(self.customer1)
        response = self.client.get(reverse("dashboard:overview"))
        self.assertEqual(response.status_code, 403)

    def test_authorized_staff_can_access_management(self):
        """Authorized staff user can access /management/ overview."""
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("dashboard:overview"))
        self.assertEqual(response.status_code, 200)

    def test_customer_cannot_view_another_customers_order(self):
        """Customer isolation: Customer 2 cannot access Customer 1's order details."""
        order1 = Order.objects.create(
            order_number="ZY-CUST1-ORDER",
            user=self.customer1,
            email=self.customer1.email,
            phone="1234567890",
            status=Order.Status.PAID,
            subtotal=1000,
            total_amount=1000,
            shipping_full_name="Cust One",
            shipping_address_line_1="Addr 1",
            shipping_city="City",
            shipping_state="State",
            shipping_postal_code="123456",
        )

        self.client.force_login(self.customer2)
        response = self.client.get(reverse("orders:order_detail", kwargs={"order_number": order1.order_number}))
        # Redirected away with error message
        self.assertEqual(response.status_code, 302)
