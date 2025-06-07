"""Admin configuration for the Greenova core app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from beartype import beartype
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
    EnvironmentalObligationForm,
    UserProfileForm,
)
from .models import (
    AuditLog,
    CustomUser,
    EnvironmentalObligation,
    UserProfile,
)


@admin.register(EnvironmentalObligation)
class EnvironmentalObligationAdmin(admin.ModelAdmin):  # type: ignore[misc]
    """Admin for EnvironmentalObligation with autocomplete support."""

    form = EnvironmentalObligationForm
    search_fields = ["name", "description"]
    list_display = ("name", "due_date", "is_complete")
    list_filter = ("is_complete", "due_date")


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):  # type: ignore[misc]
    """Admin for CustomUser with custom creation and change forms."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ("username", "email", "company", "is_mfa_enabled", "is_active")
    search_fields = ("username", "email", "company")
    list_filter = ("is_active", "is_mfa_enabled")
    ordering = ("username",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):  # type: ignore[misc]
    """Admin for UserProfile with search and display options."""

    form = UserProfileForm
    list_display = ("user", "display_name", "updated_at")
    search_fields = ("user__username", "display_name")
    ordering = ("user__username",)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):  # type: ignore[misc]
    """Admin for AuditLog entries with optimized queryset and filters."""

    list_display = (
        "timestamp",
        "user",
        "action",
        "object_type",
        "object_id",
        "ip_address",
    )
    search_fields = ("user__username", "action", "object_type", "object_id", "message")
    list_filter = ("action", "object_type", "timestamp")
    ordering = ("-timestamp",)
    readonly_fields = ("timestamp",)

    @beartype
    def get_queryset(self, request: HttpRequest) -> QuerySet[AuditLog]:
        """Optimize queryset for audit log admin."""
        qs = super().get_queryset(request)
        return qs.select_related("user")
