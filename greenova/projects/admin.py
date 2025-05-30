"""Copyright (C) 2025 Adrian Gallo.

This file is part of Greenova.

Greenova is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Greenova is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Greenova. If not, see <https://www.gnu.org/licenses/>.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

"""Admin configuration for the projects app.

This module registers the Project and ProjectMembership models and customizes
their admin interface.
"""
from django.http import HttpRequest
from django.core.exceptions import PermissionDenied
from django.contrib import admin
from logging import getLogger
from typing import TypeVar


logger = getLogger(__name__)

T = TypeVar("T")


class BaseModelAdmin[T](admin.ModelAdmin):
    """Base admin class with type safety."""

    def dispatch(
        self, request: HttpRequest, object_id: str, from_field: None = None,
    ) -> T | None:
        """Dispatch method with permission check for admin objects."""
        obj = super().get_object(request, object_id, from_field)
        if obj and not self.has_view_or_change_permission(request, obj):
            logger.warning(
                "Permission denied for user %s on object %s",
                request.user,
                object_id,
            )
            msg = "You do not have permission to access this object."
            raise PermissionDenied(
                msg,
            )
        return obj
