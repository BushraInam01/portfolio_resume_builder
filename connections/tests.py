from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Connection
from portfolios.models import Portfolio


User = get_user_model()


class ConnectionViewsTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            email="user1@example.com",
            password="TestPassword123!",
        )

        self.user2 = User.objects.create_user(
            email="user2@example.com",
            password="TestPassword123!",
        )

        self.user3 = User.objects.create_user(
            email="user3@example.com",
            password="TestPassword123!",
        )

        self.portfolio1 = Portfolio.objects.create(
            user=self.user1,
            title="User 1 Portfolio",
            slug="user-1-portfolio",
            is_public=True,
        )

        self.portfolio2 = Portfolio.objects.create(
            user=self.user2,
            title="User 2 Portfolio",
            slug="user-2-portfolio",
            is_public=True,
        )

        self.portfolio3 = Portfolio.objects.create(
            user=self.user3,
            title="User 3 Portfolio",
            slug="user-3-portfolio",
            is_public=True,
        )

        self.list_url = reverse("connections:list")

        self.send_url = reverse(
            "connections:send_request",
            kwargs={"user_id": self.user2.pk},
        )

    def login_user(self, user):
        self.client.login(
            email=user.email,
            password="TestPassword123!",
        )

    def action_url(self, connection, action):
        return reverse(
            "connections:request_action",
            kwargs={
                "connection_id": connection.pk,
                "action": action,
            },
        )

    def test_anonymous_user_cannot_access_connections(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_authenticated_user_can_access_connections(self):
        self.login_user(self.user1)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "connections/connection_list.html",
        )

    def test_user_can_send_connection_request(self):
        self.login_user(self.user1)

        response = self.client.post(self.send_url)

        self.assertRedirects(response, self.list_url)

        self.assertTrue(
            Connection.objects.filter(
                requester=self.user1,
                receiver=self.user2,
                status=Connection.Status.PENDING,
            ).exists()
        )

    def test_duplicate_connection_request_is_prevented(self):
        self.login_user(self.user1)

        Connection.objects.create(
            requester=self.user1,
            receiver=self.user2,
        )

        self.client.post(self.send_url)

        self.assertEqual(
            Connection.objects.filter(
                requester=self.user1,
                receiver=self.user2,
            ).count(),
            1,
        )

    def test_reverse_pending_request_is_prevented(self):
        Connection.objects.create(
            requester=self.user2,
            receiver=self.user1,
            status=Connection.Status.PENDING,
        )

        self.login_user(self.user1)

        self.client.post(self.send_url)

        self.assertFalse(
            Connection.objects.filter(
                requester=self.user1,
                receiver=self.user2,
            ).exists()
        )

    def test_reverse_accepted_connection_is_prevented(self):
        Connection.objects.create(
            requester=self.user2,
            receiver=self.user1,
            status=Connection.Status.ACCEPTED,
        )

        self.login_user(self.user1)

        self.client.post(self.send_url)

        self.assertFalse(
            Connection.objects.filter(
                requester=self.user1,
                receiver=self.user2,
            ).exists()
        )

    def test_user_cannot_send_request_to_themselves(self):
        self.login_user(self.user1)

        self_url = reverse(
            "connections:send_request",
            kwargs={"user_id": self.user1.pk},
        )

        response = self.client.post(self_url)

        self.assertRedirects(response, self.list_url)
        self.assertEqual(Connection.objects.count(), 0)

    def test_private_portfolio_user_cannot_receive_request(self):
        self.portfolio2.is_public = False
        self.portfolio2.save()

        self.login_user(self.user1)

        response = self.client.post(self.send_url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Connection.objects.count(), 0)

    def test_inactive_user_cannot_receive_request(self):
        self.user2.is_active = False
        self.user2.save()

        self.login_user(self.user1)

        response = self.client.post(self.send_url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Connection.objects.count(), 0)

    def test_rejected_request_can_be_sent_again(self):
        connection = Connection.objects.create(
            requester=self.user1,
            receiver=self.user2,
            status=Connection.Status.REJECTED,
        )

        self.login_user(self.user1)

        response = self.client.post(self.send_url)

        connection.refresh_from_db()

        self.assertRedirects(response, self.list_url)
        self.assertEqual(
            connection.status,
            Connection.Status.PENDING,
        )
        self.assertEqual(Connection.objects.count(), 1)

    def test_receiver_can_accept_request(self):
        connection = Connection.objects.create(
            requester=self.user1,
            receiver=self.user2,
        )

        self.login_user(self.user2)

        response = self.client.post(
            self.action_url(connection, "accept")
        )

        connection.refresh_from_db()

        self.assertRedirects(response, self.list_url)
        self.assertEqual(
            connection.status,
            Connection.Status.ACCEPTED,
        )

    def test_receiver_can_reject_request(self):
        connection = Connection.objects.create(
            requester=self.user1,
            receiver=self.user2,
        )

        self.login_user(self.user2)

        response = self.client.post(
            self.action_url(connection, "reject")
        )

        connection.refresh_from_db()

        self.assertRedirects(response, self.list_url)
        self.assertEqual(
            connection.status,
            Connection.Status.REJECTED,
        )

    def test_requester_can_cancel_pending_request(self):
        connection = Connection.objects.create(
            requester=self.user1,
            receiver=self.user2,
        )

        self.login_user(self.user1)

        response = self.client.post(
            self.action_url(connection, "cancel")
        )

        self.assertRedirects(response, self.list_url)
        self.assertFalse(
            Connection.objects.filter(pk=connection.pk).exists()
        )

    def test_either_user_can_remove_accepted_connection(self):
        connection = Connection.objects.create(
            requester=self.user1,
            receiver=self.user2,
            status=Connection.Status.ACCEPTED,
        )

        self.login_user(self.user2)

        response = self.client.post(
            self.action_url(connection, "remove")
        )

        self.assertRedirects(response, self.list_url)
        self.assertFalse(
            Connection.objects.filter(pk=connection.pk).exists()
        )

    def test_non_receiver_cannot_accept_request(self):
        connection = Connection.objects.create(
            requester=self.user1,
            receiver=self.user2,
        )

        self.login_user(self.user3)

        response = self.client.post(
            self.action_url(connection, "accept")
        )

        connection.refresh_from_db()

        self.assertRedirects(response, self.list_url)
        self.assertEqual(
            connection.status,
            Connection.Status.PENDING,
        )

    def test_non_requester_cannot_cancel_request(self):
        connection = Connection.objects.create(
            requester=self.user1,
            receiver=self.user2,
        )

        self.login_user(self.user3)

        response = self.client.post(
            self.action_url(connection, "cancel")
        )

        self.assertRedirects(response, self.list_url)
        self.assertTrue(
            Connection.objects.filter(pk=connection.pk).exists()
        )

    def test_non_connection_user_cannot_remove_connection(self):
        connection = Connection.objects.create(
            requester=self.user1,
            receiver=self.user2,
            status=Connection.Status.ACCEPTED,
        )

        self.login_user(self.user3)

        response = self.client.post(
            self.action_url(connection, "remove")
        )

        self.assertRedirects(response, self.list_url)
        self.assertTrue(
            Connection.objects.filter(pk=connection.pk).exists()
        )

    def test_invalid_action_does_not_change_connection(self):
        connection = Connection.objects.create(
            requester=self.user1,
            receiver=self.user2,
            status=Connection.Status.PENDING,
        )

        self.login_user(self.user2)

        response = self.client.post(
            self.action_url(connection, "invalid")
        )

        connection.refresh_from_db()

        self.assertRedirects(response, self.list_url)
        self.assertEqual(
            connection.status,
            Connection.Status.PENDING,
        )

    def test_get_request_cannot_send_connection_request(self):
        self.login_user(self.user1)

        response = self.client.get(self.send_url)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(Connection.objects.count(), 0)

    def test_get_request_cannot_accept_connection(self):
        connection = Connection.objects.create(
            requester=self.user1,
            receiver=self.user2,
        )

        self.login_user(self.user2)

        response = self.client.get(
            self.action_url(connection, "accept")
        )

        self.assertEqual(response.status_code, 405)

        connection.refresh_from_db()

        self.assertEqual(
            connection.status,
            Connection.Status.PENDING,
        )