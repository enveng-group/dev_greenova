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

# Import the Company model
from .models import Company

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


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_type', 'industry', 'is_active', 'created_at')
    list_filter = ('company_type', 'industry', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'logo')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'website', 'address')
        }),
        ('Classification', {
            'fields': ('company_type', 'industry', 'size')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
