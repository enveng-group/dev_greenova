"""Admin configuration for the Procedures app.

This module customizes the Django admin interface for the Procedure model,
including permission checks and admin actions.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any

from beartype import beartype
from django.contrib import admin
from django.http import HttpRequest

from .models import Procedure
from .permissions import user_can_view_procedure


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    """Admin configuration for the Procedure model."""

    list_display = ("name", "description")
    search_fields = ("name", "description")
    list_filter = ("name",)

    @beartype
    def get_queryset(self, request: HttpRequest) -> Any:
        """Get the queryset for the admin list view.

        Args:
            request: The HTTP request object.

        Returns:
            The queryset of Procedure objects.

        """
        return super().get_queryset(request)

    @beartype
    def has_view_permission(
        self,
        request: HttpRequest,
        obj: Procedure | None = None,
    ) -> bool:
        """Check if the user has permission to view the procedure.

        Args:
            request: The HTTP request object.
            obj: The Procedure instance (optional).

        Returns:
            True if the user can view, False otherwise.

        """
        if obj is not None:
            return user_can_view_procedure(request.user, obj)
        return super().has_view_permission(request, obj=obj)

    @beartype
    def has_change_permission(
        self,
        request: HttpRequest,
        obj: Procedure | None = None,
    ) -> bool:
        """Check if the user has permission to change the procedure.

        Args:
            request: The HTTP request object.
            obj: The Procedure instance (optional).

        Returns:
            True if the user can change, False otherwise.

        """
        return super().has_change_permission(request, obj=obj)

    @beartype
    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: Procedure | None = None,
    ) -> bool:
        """Check if the user has permission to delete the procedure.

        Args:
            request: The HTTP request object.
            obj: The Procedure instance (optional).

        Returns:
            True if the user can delete, False otherwise.

        """
        return super().has_delete_permission(request, obj=obj)
