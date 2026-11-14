from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from connections.models import Connection
from portfolios.models import Portfolio, Skill
from .models import Endorsement


User = get_user_model()


class EndorseSkillViewTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@example.com",
            password="TestPassword123!",
        )

        self.endorser = User.objects.create_user(
            email="endorser@example.com",
            password="TestPassword123!",
        )

        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="TestPassword123!",
        )

        self.portfolio = Portfolio.objects.create(
            user=self.owner,
            title="Owner Portfolio",
            slug="owner-portfolio",
            full_name="Portfolio Owner",
            is_public=True,
            allow_endorsements=True,
        )

        self.skill = Skill.objects.create(
            portfolio=self.portfolio,
            name="Django",
            proficiency=Skill.ProficiencyLevel.INTERMEDIATE,
        )

        self.url = reverse(
            "endorsements:endorse_skill",
            kwargs={"skill_id": self.skill.pk},
        )

        self.connection = Connection.objects.create(
            requester=self.endorser,
            receiver=self.owner,
            status=Connection.Status.ACCEPTED,
        )

    def test_accepted_connection_can_endorse_skill(self):
        self.client.login(
            email="endorser@example.com",
            password="TestPassword123!",
        )

        response = self.client.post(self.url)

        self.assertRedirects(
            response,
            reverse(
                "portfolios:public_detail",
                kwargs={"slug": self.portfolio.slug},
            ),
        )

        self.assertTrue(
            Endorsement.objects.filter(
                skill=self.skill,
                endorser=self.endorser,
            ).exists()
        )

        self.assertEqual(self.skill.endorsements.count(), 1)

    def test_duplicate_endorsement_is_not_created(self):
        self.client.login(
            email="endorser@example.com",
            password="TestPassword123!",
        )

        Endorsement.objects.create(
            skill=self.skill,
            endorser=self.endorser,
        )

        response = self.client.post(self.url, follow=True)

        self.assertRedirects(
            response,
            reverse(
                "portfolios:public_detail",
                kwargs={"slug": self.portfolio.slug},
            ),
        )

        self.assertEqual(self.skill.endorsements.count(), 1)

        self.assertContains(
            response,
            "You have already endorsed this skill.",
        )
    def test_portfolio_owner_cannot_endorse_own_skill(self):
        self.client.login(
            email="owner@example.com",
            password="TestPassword123!",
        )

        response = self.client.post(self.url)

        self.assertRedirects(
            response,
            reverse(
                "portfolios:public_detail",
                kwargs={"slug": self.portfolio.slug},
            ),
        )

        self.assertEqual(self.skill.endorsements.count(), 0)

    def test_non_connection_cannot_endorse_skill(self):
        self.client.login(
            email="other@example.com",
            password="TestPassword123!",
        )

        response = self.client.post(self.url)

        self.assertRedirects(
            response,
            reverse(
                "portfolios:public_detail",
                kwargs={"slug": self.portfolio.slug},
            ),
        )

        self.assertEqual(self.skill.endorsements.count(), 0)

    def test_pending_connection_cannot_endorse_skill(self):
        self.connection.status = Connection.Status.PENDING
        self.connection.save()

        self.client.login(
            email="endorser@example.com",
            password="TestPassword123!",
        )

        response = self.client.post(self.url)

        self.assertRedirects(
            response,
            reverse(
                "portfolios:public_detail",
                kwargs={"slug": self.portfolio.slug},
            ),
        )

        self.assertEqual(self.skill.endorsements.count(), 0)

    def test_private_portfolio_skill_cannot_be_endorsed(self):
        self.portfolio.is_public = False
        self.portfolio.save()

        self.client.login(
            email="endorser@example.com",
            password="TestPassword123!",
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.skill.endorsements.count(), 0)

    def test_disabled_endorsements_are_rejected(self):
        self.portfolio.allow_endorsements = False
        self.portfolio.save()

        self.client.login(
            email="endorser@example.com",
            password="TestPassword123!",
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.skill.endorsements.count(), 0)

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

        self.assertEqual(self.skill.endorsements.count(), 0)

    def test_get_request_is_not_allowed(self):
        self.client.login(
            email="endorser@example.com",
            password="TestPassword123!",
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(self.skill.endorsements.count(), 0)
