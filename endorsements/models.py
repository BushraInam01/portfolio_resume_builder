from django.conf import settings
from django.db import models


class Endorsement(models.Model):
    """Store skill endorsements given by connected users."""

    skill = models.ForeignKey(
        "portfolios.Skill",
        on_delete=models.CASCADE,
        related_name="endorsements",
    )

    endorser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="given_endorsements",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["skill", "endorser"],
                name="unique_skill_endorsement",
            ),
        ]

    def __str__(self):
        return (
            f"{self.endorser.email} endorsed "
            f"{self.skill.name}"
        )

