
from django.contrib import admin

from .models import Endorsement


@admin.register(Endorsement)
class EndorsementAdmin(admin.ModelAdmin):

    list_display = (
        "skill",
        "endorser",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "skill__name",
        "endorser__email",
        "skill__portfolio__user__email",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = ("-created_at",)

