<<<<<<< HEAD
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
=======
from django.contrib import admin
from .models import Company, CompanyMembership, CompanyDocument


class CompanyMembershipInline(admin.TabularInline):
    model = CompanyMembership
    extra = 1
    raw_id_fields = ('user',)


class CompanyDocumentInline(admin.TabularInline):
    model = CompanyDocument
    extra = 1
    raw_id_fields = ('uploaded_by',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_type', 'industry', 'is_active', 'get_member_count')
    list_filter = ('company_type', 'industry', 'is_active')
    search_fields = ('name', 'description', 'website')
    inlines = (CompanyMembershipInline, CompanyDocumentInline)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'logo', 'description')
        }),
        ('Contact Information', {
            'fields': ('website', 'address', 'phone', 'email')
        }),
        ('Classification', {
            'fields': ('company_type', 'size', 'industry', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CompanyMembership)
class CompanyMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'role', 'department', 'position', 'is_primary')
    list_filter = ('role', 'is_primary')
    search_fields = ('user__username', 'company__name', 'department', 'position')
    raw_id_fields = ('user', 'company')


@admin.register(CompanyDocument)
class CompanyDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'document_type', 'uploaded_by', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('name', 'description', 'company__name')
    raw_id_fields = ('company', 'uploaded_by')
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
