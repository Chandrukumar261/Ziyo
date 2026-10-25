from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationTests(TestCase):
    """Unit and integration tests for customer registration, authentication, and password security."""

    def setUp(self):
        self.client = Client()

    def test_customer_registration_success(self):
        """Tests standard customer registration with password hashing."""
        response = self.client.post(reverse("accounts:register"), {
            "email": "customer@ziyo.store",
            "first_name": "Siddharth",
            "last_name": "Verma",
            "phone": "+919876543210",
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!",
        })
        self.assertEqual(response.status_code, 302)  # Redirects to home on success
        user = User.objects.get(email="customer@ziyo.store")
        self.assertEqual(user.first_name, "Siddharth")
        self.assertEqual(user.role, User.Role.CUSTOMER)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        # Check password is never stored in plaintext
        self.assertNotEqual(user.password, "StrongPassword123!")
        self.assertTrue(user.check_password("StrongPassword123!"))

    def test_registration_password_mismatch_rejected(self):
        """Tests that mismatched passwords are error-flagged."""
        response = self.client.post(reverse("accounts:register"), {
            "email": "mismatch@ziyo.store",
            "first_name": "Test",
            "last_name": "User",
            "password": "Password123!",
            "confirm_password": "DifferentPassword123!",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "confirm_password", "Passwords do not match.")
        self.assertFalse(User.objects.filter(email="mismatch@ziyo.store").exists())

    def test_customer_login_and_logout(self):
        """Tests login verification and session destruction on logout."""
        user = User.objects.create_user(
            email="client@ziyo.store",
            password="SecureSecretPassword456!",
            first_name="Ravi",
        )
        login_resp = self.client.post(reverse("accounts:login"), {
            "email": "client@ziyo.store",
            "password": "SecureSecretPassword456!",
        })
        self.assertEqual(login_resp.status_code, 302)
        # Verify authenticated session
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.id) if isinstance(user.id, int) else self.assertEqual(self.client.session["_auth_user_id"], str(user.id))

        # Logout
        logout_resp = self.client.post(reverse("accounts:logout"))
        self.assertEqual(logout_resp.status_code, 302)
        self.assertNotIn("_auth_user_id", self.client.session)
