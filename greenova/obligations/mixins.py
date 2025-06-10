"""Mixins for obligations views.

Provides reusable mixins for obligations views with proper permissions,
context data, and common functionality.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import logging
from typing import Any

from beartype import beartype
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest

logger = logging.getLogger(__name__)


class ObligationContextMixin:
    """Mixin to provide common context data for obligation views."""

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add common obligation context data.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Context dictionary with obligation-specific data.

        """
        context = super().get_context_data(**kwargs)  # type: ignore[misc]

        # Add any common context variables here
        context["app_name"] = "obligations"

        return context


class ObligationPermissionRequiredMixin(PermissionRequiredMixin):
    """Mixin to require permissions for obligation operations."""

    # Default permission for viewing obligations
    permission_required = "obligations.view_obligation"

    @beartype
    def has_permission(self) -> bool:
        """Check if the user has the required permissions.

        Returns:
            True if user has permission, False otherwise.

        """
        perms = self.get_permission_required()
        if hasattr(self, "get_object"):
            # For object-level permissions
            try:
                obj = self.get_object()  # type: ignore[attr-defined]
                return self.request.user.has_perms(
                    perms, obj)  # type: ignore[attr-defined]
            except (Http404, AttributeError):
                # Fall back to model-level permissions
                pass

        return self.request.user.has_perms(perms)  # type: ignore[attr-defined]

    @beartype
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        """Dispatch the request after checking permissions.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The response from the parent dispatch method.

        Raises:
            PermissionDenied: If the user lacks required permissions.

        """
        if not self.has_permission():
            msg = "You don't have permission to access this resource."
            raise PermissionDenied(msg)

        return super().dispatch(request, *args, **kwargs)  # type: ignore[misc]
