from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Portfolio, PortfolioSection


def create_default_sections(portfolio_id, using="default"):
    """
    Create default sections for a portfolio if they do not exist.
    """

    portfolio = Portfolio.objects.using(using).filter(
        pk=portfolio_id
    ).first()

    if portfolio is None:
        return

    for order, (section_type, _) in enumerate(
        PortfolioSection.SectionType.choices
    ):
        PortfolioSection.objects.using(using).get_or_create(
            portfolio_id=portfolio.pk,
            section_type=section_type,
            defaults={
                "sort_order": order,
                "is_visible": True,
            },
        )


@receiver(post_save, sender=Portfolio)
def create_default_portfolio_sections(
    sender,
    instance,
    created,
    raw=False,
    using="default",
    **kwargs,
):
    """
    Create default sections whenever a new portfolio is saved.
    """

    if not created:
        return

    if raw:
        transaction.on_commit(
            lambda: create_default_sections(instance.pk, using),
            using=using,
        )
        return

    create_default_sections(instance.pk, using)