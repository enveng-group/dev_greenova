"""Admin configuration for the Greenova core app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from beartype import beartype
from django.contrib import admin

from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
    EnvironmentalObligationForm,
    UserProfileForm,
)
from .models import AuditLog, CustomUser, EnvironmentalObligation, UserProfile


@admin.register(EnvironmentalObligation)
@beartype
class EnvironmentalObligationAdmin(admin.ModelAdmin):
    """Admin for EnvironmentalObligation model."""

    form = EnvironmentalObligationForm
    list_display = ("name", "due_date", "is_complete", "created_at", "updated_at")
    list_filter = ("is_complete", "due_date")
    search_fields = ("name", "description")


@admin.register(CustomUser)
@beartype
class CustomUserAdmin(admin.ModelAdmin):
    """Admin for CustomUser model."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = (
        "username",
        "email",
        "is_mfa_enabled",
        "company",
        "is_staff",
        "is_active",
    )
    search_fields = ("username", "email", "company")
    list_filter = ("is_mfa_enabled", "is_staff", "is_active")


@admin.register(UserProfile)
@beartype
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile model."""

    form = UserProfileForm
    list_display = ("user", "display_name", "updated_at")
    search_fields = ("user__username", "display_name")


@admin.register(AuditLog)
@beartype
class AuditLogAdmin(admin.ModelAdmin):
    """Admin for AuditLog model."""

    list_display = (
        "timestamp",
        "user",
        "action",
        "object_type",
        "object_id",
        "ip_address",
    )
    search_fields = (
        "user__username",
        "action",
        "object_type",
        "object_id",
        "ip_address",
    )
    list_filter = ("action", "object_type", "timestamp")
