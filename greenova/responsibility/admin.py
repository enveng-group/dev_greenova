"""
Admin configuration for the responsibility app.

This module registers the Responsibility and ResponsibilityAssignment models
and customizes their admin interface.
"""

from django.contrib import admin

from .models import Responsibility, ResponsibilityAssignment


@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    """Admin configuration for Responsibility model."""
    list_display = ("name", "description")
    search_fields = ("name", "description")


@admin.register(ResponsibilityAssignment)
class ResponsibilityAssignmentAdmin(admin.ModelAdmin):
    """Admin configuration for ResponsibilityAssignment model."""
    list_display = ("user", "obligation", "role", "created_by", "created_at")
    list_filter = ("role", "created_at")
    search_fields = ("user__username", "user__email", "obligation__obligation_number")
    raw_id_fields = ("user", "obligation", "role", "created_by")
