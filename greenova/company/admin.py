# Standard library imports
from __future__ import annotations

import logging
from typing import Any

# Third-party imports
# Third-party imports
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.db.models import Model
from django.http import HttpRequest

# Configure logger
logger = logging.getLogger(__name__)

class BaseModelAdmin(admin.ModelAdmin):
    """Base admin class with type safety."""

    def dispatch(
        self,
        request: HttpRequest,
        object_id: Any,
        from_field: str | None = None
    ) -> Model | None:
        """Get object with type safety and permission checking."""
        obj = super().get_object(
            request,
            object_id,
            from_field
        )

        # Implement permission check
        if obj is not None and not self.has_view_permission(
            request,
            obj
        ):
            logger.warning(
                (
                    'Permission denied: User %s attempted to access %s '
                    'without sufficient permissions.'
                ),
                request.user,
                obj
            )
            raise PermissionDenied(
                'You do not have permission to view this object. '
                'Please contact the administrator if you believe this is an error.'
            )

        return obj
