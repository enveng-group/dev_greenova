# Standard library imports
from __future__ import annotations

import logging
from typing import Any, Optional

# Django imports
from django.contrib import admin
from django.db.models import Model
from django.http import HttpRequest

# Configure logger
logger = logging.getLogger(__name__)

class BaseModelAdmin(admin.ModelAdmin):
    """Base admin class with type safety."""

    def get_object(self, request: HttpRequest, object_id: Any, from_field: str | None = None) -> Model | None:
        """Get object with type safety and permission checking."""
        obj = super().get_object(request, object_id, from_field)

        # Implement permission check
        if obj is not None and not self.has_view_permission(request, obj):
            return None

        return obj
