from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from connections.models import Connection
from portfolios.models import Skill

from .models import Endorsement


class EndorseSkillView(LoginRequiredMixin, View):
    """Allow an accepted connection to endorse a skill."""

    def post(self, request, skill_id, *args, **kwargs):
        skill = get_object_or_404(
            Skill.objects.select_related("portfolio", "portfolio__user"),
            pk=skill_id,
            portfolio__is_public=True,
            portfolio__allow_endorsements=True,
        )

        portfolio = skill.portfolio
        owner = portfolio.user

        # Portfolio owner cannot endorse their own skills.
        if request.user == owner:
            messages.error(
                request,
                "You cannot endorse your own skills.",
            )
            return redirect(
                "portfolios:public_detail",
                slug=portfolio.slug,
            )

        # Only accepted connections can endorse.
        is_connected = Connection.objects.filter(
            Q(requester=request.user, receiver=owner)
            | Q(requester=owner, receiver=request.user),
            status=Connection.Status.ACCEPTED,
        ).exists()

        if not is_connected:
            messages.error(
                request,
                "Only accepted connections can endorse this skill.",
            )
            return redirect(
                "portfolios:public_detail",
                slug=portfolio.slug,
            )

        endorsement, created = Endorsement.objects.get_or_create(
            skill=skill,
            endorser=request.user,
        )

        if created:
            messages.success(
                request,
                f"You successfully endorsed {skill.name}.",
            )
        else:
            messages.info(
                request,
                "You have already endorsed this skill.",
            )

        return redirect(
            "portfolios:public_detail",
            slug=portfolio.slug,
        )
