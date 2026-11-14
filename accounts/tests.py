from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class AuthenticationTestCase(TestCase):
    """Shared setup for authentication tests."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="existing@example.com",
            password="Existing!SecurePass2026",
            first_name="Test",
            last_name="User",
        )


class RegistrationTests(AuthenticationTestCase):
    def test_user_can_register(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "email": "newuser@example.com",
                "first_name": "New",
                "last_name": "User",
                "password1": "New!SecurePass2026",
                "password2": "New!SecurePass2026",
            },
        )

        self.assertRedirects(
            response,
            reverse("accounts:login"),
        )

        new_user = User.objects.get(
            email="newuser@example.com"
        )

        self.assertTrue(
            new_user.check_password("New!SecurePass2026")
        )

    def test_duplicate_email_registration_is_rejected(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "email": "existing@example.com",
                "first_name": "Duplicate",
                "last_name": "User",
                "password1": "New!SecurePass2026",
                "password2": "New!SecurePass2026",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "An account with this email already exists.",
        )

        self.assertEqual(User.objects.count(), 1)

    def test_password_mismatch_is_rejected(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "email": "mismatch@example.com",
                "first_name": "Test",
                "last_name": "User",
                "password1": "First!SecurePass2026",
                "password2": "Second!SecurePass2026",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(
                email="mismatch@example.com"
            ).exists()
        )


class LoginTests(AuthenticationTestCase):
    def test_user_can_login_with_email(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "existing@example.com",
                "password": "Existing!SecurePass2026",
            },
        )

        self.assertRedirects(
            response,
            reverse("accounts:dashboard"),
        )

    def test_invalid_credentials_are_rejected(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "existing@example.com",
                "password": "WrongPassword123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            "_auth_user_id",
            self.client.session,
        )


class DashboardAccessTests(AuthenticationTestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(
            reverse("accounts:dashboard")
        )

        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('accounts:dashboard')}",
        )

    def test_authenticated_user_can_access_dashboard(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("accounts:dashboard")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "existing@example.com")


class LogoutTests(AuthenticationTestCase):
    def test_user_can_logout(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("accounts:logout")
        )

        self.assertRedirects(
            response,
            reverse("accounts:login"),
        )

        self.assertNotIn(
            "_auth_user_id",
            self.client.session,
        )


class PasswordChangeTests(AuthenticationTestCase):
    def test_user_can_change_password(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("accounts:password_change"),
            {
                "old_password": "Existing!SecurePass2026",
                "new_password1": "Updated!SecurePass2026",
                "new_password2": "Updated!SecurePass2026",
            },
        )

        self.assertRedirects(
            response,
            reverse("accounts:password_change_done"),
        )

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.check_password("Updated!SecurePass2026")
        )


class PasswordResetTests(AuthenticationTestCase):
    def test_password_reset_request_sends_email(self):
        from django.core import mail

        response = self.client.post(
            reverse("accounts:password_reset"),
            {
                "email": "existing@example.com",
            },
        )

        self.assertRedirects(
            response,
            reverse("accounts:password_reset_done"),
        )

        self.assertEqual(len(mail.outbox), 1)

        self.assertIn(
            "Password Reset",
            mail.outbox[0].subject,
        )

