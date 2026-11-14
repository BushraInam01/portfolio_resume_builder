from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from .models import Connection


User = get_user_model()


class ConnectionListView(LoginRequiredMixin, ListView):
    """Display connections, requests and discoverable public portfolios."""

    model = Connection
    template_name = "connections/connection_list.html"
    context_object_name = "connections"

    def get_queryset(self):
        return Connection.objects.filter(
            Q(requester=self.request.user)
            | Q(receiver=self.request.user),
            status=Connection.Status.ACCEPTED,
        ).select_related("requester", "receiver")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["received_requests"] = Connection.objects.filter(
            receiver=self.request.user,
            status=Connection.Status.PENDING,
        ).select_related("requester")

        context["sent_requests"] = Connection.objects.filter(
            requester=self.request.user,
            status=Connection.Status.PENDING,
        ).select_related("receiver")

        context["discoverable_users"] = (
            User.objects.filter(
                is_active=True,
                portfolio__is_public=True,
            )
            .exclude(pk=self.request.user.pk)
            .select_related("portfolio")
        )

        return context


class SendConnectionRequestView(LoginRequiredMixin, View):
    """Send a connection request to a user with a public portfolio."""

    def post(self, request, user_id, *args, **kwargs):
        receiver = get_object_or_404(
            User.objects.filter(
                is_active=True,
                portfolio__is_public=True,
            ),
            pk=user_id,
        )

        if receiver == request.user:
            messages.error(request, "You cannot connect with yourself.")
            return redirect("connections:list")

        reverse_request = Connection.objects.filter(
            requester=receiver,
            receiver=request.user,
            status__in=[
                Connection.Status.PENDING,
                Connection.Status.ACCEPTED,
            ],
        ).exists()

        if reverse_request:
            messages.warning(
                request,
                "A connection request or connection already exists.",
            )
            return redirect("connections:list")

        try:
            with transaction.atomic():
                existing_request = Connection.objects.filter(
                    requester=request.user,
                    receiver=receiver,
                ).first()

                if existing_request:
                    if existing_request.status == Connection.Status.REJECTED:
                        existing_request.status = Connection.Status.PENDING
                        existing_request.save(
                            update_fields=["status", "updated_at"]
                        )
                        messages.success(
                            request,
                            "Connection request sent successfully.",
                        )
                    else:
                        messages.warning(
                            request,
                            "A request already exists.",
                        )
                else:
                    Connection.objects.create(
                        requester=request.user,
                        receiver=receiver,
                    )
                    messages.success(
                        request,
                        "Connection request sent successfully.",
                    )

        except IntegrityError:
            messages.warning(
                request,
                "A connection request already exists.",
            )

        return redirect("connections:list")


class ConnectionRequestActionView(LoginRequiredMixin, View):
    """Accept, reject, cancel or remove a connection."""

    def post(self, request, connection_id, action, *args, **kwargs):
        connection = get_object_or_404(
            Connection,
            pk=connection_id,
        )

        if action == "accept":
            if (
                connection.receiver != request.user
                or connection.status != Connection.Status.PENDING
            ):
                messages.error(request, "You cannot accept this request.")
            else:
                connection.status = Connection.Status.ACCEPTED
                connection.save(
                    update_fields=["status", "updated_at"]
                )
                messages.success(request, "Connection accepted.")

        elif action == "reject":
            if (
                connection.receiver != request.user
                or connection.status != Connection.Status.PENDING
            ):
                messages.error(request, "You cannot reject this request.")
            else:
                connection.status = Connection.Status.REJECTED
                connection.save(
                    update_fields=["status", "updated_at"]
                )
                messages.success(request, "Connection request rejected.")

        elif action == "cancel":
            if (
                connection.requester != request.user
                or connection.status != Connection.Status.PENDING
            ):
                messages.error(request, "You cannot cancel this request.")
            else:
                connection.delete()
                messages.success(request, "Connection request cancelled.")

        elif action == "remove":
            if (
                request.user not in [
                    connection.requester,
                    connection.receiver,
                ]
                or connection.status != Connection.Status.ACCEPTED
            ):
                messages.error(request, "You cannot remove this connection.")
            else:
                connection.delete()
                messages.success(request, "Connection removed.")

        else:
            messages.error(request, "Invalid connection action.")

        return redirect("connections:list")
