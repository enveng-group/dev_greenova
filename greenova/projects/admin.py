"""
Admin configuration for the projects app.

This module registers the Project and ProjectMembership models and customizes
their admin interface.
"""
from logging import getLogger
from typing import Generic, TypeVar

from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest

logger = getLogger(__name__)

T = TypeVar("T")


class BaseModelAdmin(admin.ModelAdmin, Generic[T]):
    """Base admin class with type safety."""

    def dispatch(
        self, request: HttpRequest, object_id: str, from_field: None = None
    ) -> T | None:
        """Dispatch method with permission check for admin objects."""
        obj = super().get_object(request, object_id, from_field)
        if obj:
            if not self.has_view_or_change_permission(request, obj):
                logger.warning(
                    "Permission denied for user %s on object %s",
                    request.user,
                    object_id,
                )
                raise PermissionDenied(
                    "You do not have permission to access this object."
                )
        return obj
