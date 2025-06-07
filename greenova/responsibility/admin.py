"""Admin configuration for the Responsibility app.

This module customizes the Django admin interface for the Responsibility model,
including syncing from core roles and enforcing referential integrity.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any

from beartype import beartype
from core.utils.roles import get_responsibility_choices
from django.contrib import admin, messages
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import path, reverse

from .models import Responsibility


@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    """Admin configuration for Responsibility model."""

    list_display = ("name", "description")
    list_filter = ("name",)
    search_fields = ("name", "description")

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "description"),
            },
        ),
    )

    @beartype
    def get_readonly_fields(
        self,
        request: HttpRequest,
        obj: Responsibility | None = None,
    ) -> tuple[str, ...]:
        """Make name field readonly after creation to maintain referential integrity.

        Args:
            request: The HTTP request object.
            obj: The Responsibility instance (optional).

        Returns:
            A tuple of readonly field names.

        """
        if obj:
            return ("name",)
        return ()

    @beartype
    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: Responsibility | None = None,
    ) -> bool:
        """Prevent deletion of responsibility values to maintain referential integrity.

        Args:
            request: The HTTP request object.
            obj: The Responsibility instance (optional).

        Returns:
            True if deletion is allowed, False otherwise.

        """
        if obj:
            from obligations.models import Obligation

            if Obligation.objects.filter(responsibility=obj.name).exists():
                return False
        return True

    @beartype
    def get_urls(self) -> list[Any]:
        """Get custom admin URLs for ResponsibilityAdmin.

        Returns:
            A list of URL patterns.

        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "sync-from-roles/",
                self.sync_from_roles,
                name="responsibility_sync_from_roles",
            ),
        ]
        return custom_urls + urls

    @beartype
    def sync_from_roles(self, request: HttpRequest) -> HttpResponseRedirect:
        """Sync responsibility values from core.utils.roles.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponseRedirect to the responsibility changelist.

        """
        try:
            choices = get_responsibility_choices()
            count = 0
            for _value, display_name in choices:
                if not Responsibility.objects.filter(name=display_name).exists():
                    Responsibility.objects.create(
                        name=display_name,
                        description=f"Auto-generated from roles system: {display_name}",
                    )
                    count += 1
            self.message_user(
                request,
                f"Successfully synced {count} new responsibilities from roles configuration.",
                messages.SUCCESS,
            )
        except Exception as e:
            self.message_user(
                request,
                f"Error syncing responsibilities: {e!s}",
                messages.ERROR,
            )
        return HttpResponseRedirect(
            reverse("admin:responsibility_responsibility_changelist"),
        )
