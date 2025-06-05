"""Admin configuration for the company app.

This module provides base admin classes and permission checks for company-related
models in the Django admin interface.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

# Standard library imports
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

# Third-party imports
from beartype import beartype
from django.contrib import admin
from django.core.exceptions import PermissionDenied

# Local imports
from .permissions import user_can_view_company

if TYPE_CHECKING:
    from django.db.models import Model
    from django.http import HttpRequest

# Configure logger
logger = logging.getLogger(__name__)


class BaseModelAdmin(admin.ModelAdmin):
    """Base admin class with type safety and permission checks."""

    @beartype
    def dispatch(
        self,
        request: "HttpRequest",
        object_id: Any,
        from_field: str | None = None,
    ) -> "Model | None":
        """Get object with type safety and permission checking.

        Args:
            request: The HTTP request object.
            object_id: The object's primary key or unique identifier.
            from_field: The field to use for lookup (optional).

        Returns:
            The model instance if found and permitted, otherwise None.

        Raises:
            PermissionDenied: If the user does not have permission to view the object.
        """
        obj = super().get_object(
            request,
            object_id,
            from_field,
        )

        # Implement permission check
        if obj is not None and not user_can_view_company(request.user, obj):
            logger.warning(
                (
                    "Permission denied: User %s attempted to access %s "
                    "without sufficient permissions."
                ),
                request.user,
                obj,
            )
            msg = (
                "You do not have permission to view this object. "
                "Please contact the administrator if you believe this is an error."
            )
            raise PermissionDenied(msg)

        return obj

    @beartype
    def has_view_permission(
        self, request: "HttpRequest", obj: "Model | None" = None
    ) -> bool:
        """Check if the user has permission to view the object.

        Args:
            request: The HTTP request object.
            obj: The model instance (optional).

        Returns:
            True if the user can view, False otherwise.
        """
        if obj is not None:
            return user_can_view_company(request.user, obj)
        return super().has_view_permission(request, obj=obj)

    @beartype
    def has_change_permission(
        self, request: "HttpRequest", obj: "Model | None" = None
    ) -> bool:
        """Check if the user has permission to change the object.

        Args:
            request: The HTTP request object.
            obj: The model instance (optional).

        Returns:
            True if the user can change, False otherwise.
        """
        if obj is not None:
            return user_can_view_company(request.user, obj)
        return super().has_change_permission(request, obj=obj)

    @beartype
    def has_delete_permission(
        self, request: "HttpRequest", obj: "Model | None" = None
    ) -> bool:
        """Check if the user has permission to delete the object.

        Args:
            request: The HTTP request object.
            obj: The model instance (optional).

        Returns:
            True if the user can delete, False otherwise.
        """
        if obj is not None:
            return user_can_view_company(request.user, obj)
        return super().has_delete_permission(request, obj=obj)
