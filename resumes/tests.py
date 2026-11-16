from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from portfolios.models import Portfolio


User = get_user_model()


class ResumeViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="resumeuser@example.com",
            password="TestPassword123!",
        )

        self.portfolio = Portfolio.objects.create(
            user=self.user,
            title="My Portfolio",
            slug="resume-user",
            full_name="Resume User",
            professional_title="Python Developer",
        )

    def test_customization_requires_login(self):
        response = self.client.get(
            reverse("resumes:customize")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            reverse("accounts:login"),
            response.url,
        )

    def test_preview_requires_login(self):
        response = self.client.get(
            reverse("resumes:preview")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            reverse("accounts:login"),
            response.url,
        )

    def test_pdf_download_requires_login(self):
        response = self.client.get(
            reverse("resumes:download_pdf")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            reverse("accounts:login"),
            response.url,
        )

    def test_customization_redirects_without_portfolio(self):
        user_without_portfolio = User.objects.create_user(
            email="noportfolio@example.com",
            password="TestPassword123!",
        )

        self.client.force_login(user_without_portfolio)

        response = self.client.get(
            reverse("resumes:customize")
        )

        self.assertRedirects(
            response,
            reverse("portfolios:portfolio_create"),
        )

    def test_theme_and_accent_color_are_saved(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("resumes:customize"),
            {
                "resume_theme": "modern",
                "accent_color": "#FF5733",
            },
        )

        self.assertRedirects(
            response,
            reverse("resumes:customize"),
        )

        self.portfolio.refresh_from_db()

        self.assertEqual(
            self.portfolio.resume_theme,
            "modern",
        )

        self.assertEqual(
            self.portfolio.accent_color,
            "#FF5733",
        )

    def test_preview_shows_own_portfolio(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("resumes:preview")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["portfolio"],
            self.portfolio,
        )

    def test_pdf_download_returns_pdf_attachment(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("resumes:download_pdf")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/pdf",
        )

        self.assertTrue(
            response.content.startswith(b"%PDF")
        )

        self.assertIn(
            'attachment; filename="resume-user-resume.pdf"',
            response["Content-Disposition"],
        )
