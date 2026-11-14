from django.conf import settings
from django.db import models
from django.db.models import Q, F


class Connection(models.Model):
    """Store connection requests and accepted connections."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_connection_requests",
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_connection_requests",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["requester", "receiver"],
                name="unique_connection_request",
            ),
            models.CheckConstraint(
                condition=~Q(requester=F("receiver")),
                name="prevent_self_connection",
            ),
        ]

    def __str__(self):
        return (
            f"{self.requester.email} -> "
            f"{self.receiver.email} ({self.status})"
        )

