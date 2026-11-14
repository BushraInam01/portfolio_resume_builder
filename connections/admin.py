
from django.contrib import admin

from .models import Connection


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):

    list_display = (
        "requester",
        "receiver",
        "status",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "requester__email",
        "receiver__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

