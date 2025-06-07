"""Admin configuration for the EnvironmentalMechanism model.

This module customizes the Django admin interface for the
EnvironmentalMechanism model, including optimized queryset, obligation count
display, and status helpers.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0

Note: All permission helpers have been migrated to core/permissions.py.
"""

from __future__ import annotations

import logging
from typing import Any, cast

from beartype import beartype
from django.contrib import admin
from django.utils import timezone

from .forms import sanitize_html
from .models import EnvironmentalMechanism

logger = logging.getLogger(__name__)


@admin.register(EnvironmentalMechanism)
class EnvironmentalMechanismAdmin(admin.ModelAdmin):  # type: ignore[misc]
    """Admin configuration for EnvironmentalMechanism model.

    Customizes the admin interface for EnvironmentalMechanism, including list
    display, filters, readonly fields, and custom obligation/status helpers.
    """

    list_display: tuple[str, ...] = (
        "name",
        "project",
        "overdue_count",
        "not_started_count",
        "in_progress_count",
        "completed_count",
        "get_total_obligations",
        "updated_at",
    )
    list_filter: tuple[str, ...] = ("project__name", "status", "updated_at")
    search_fields: tuple[str, ...] = ("name", "project__name")
    readonly_fields: tuple[str, ...] = (
        "updated_at",
        "overdue_count",
        "not_started_count",
        "in_progress_count",
        "completed_count",
        "status_chart",
        # type: ignore[attr-defined]  # Suppress type checker for dynamic
        # attribute assignment
    )
    ordering: tuple[str, ...] = ("name", "-updated_at")

    fields = (
        "name",
        "project",
        "description",
        "category",
        "reference_number",
        "effective_date",
        "status",
        "primary_environmental_mechanism",
        "updated_at",
        "overdue_count",
        "not_started_count",
        "in_progress_count",
        "completed_count",
    )

    @beartype
    def get_queryset(self, request: Any) -> Any:
        """Return a queryset optimized for admin display.

        Args:
            request: The HTTP request object.

        Returns:
            Queryset for EnvironmentalMechanism admin list view.

        """
        queryset = super().get_queryset(request)
        return cast("Any", queryset.select_related("project"))

    @staticmethod
    @beartype
    def get_total_obligations(obj: Any) -> int:
        """Return the total number of obligations for a mechanism.

        Args:
            obj: EnvironmentalMechanism instance.

        Returns:
            Total number of obligations for the mechanism.

        """
        return cast("int", obj.total_obligations)

    get_total_obligations.short_description = "Total"  # type: ignore

    @beartype
    def save_model(
        self,
        request: Any,
        obj: EnvironmentalMechanism,
        form: Any,
        change: bool,
    ) -> None:
        """Update counts when saving model in admin and sanitize description.

        Args:
            request: The HTTP request object.
            obj: The EnvironmentalMechanism instance.
            form: The model form instance.
            change: Whether this is an update.

        Returns:
            None.

        """
        if getattr(obj, "description", None):
            obj.description = sanitize_html(
                str(obj.description))  # type: ignore[assignment]
        super().save_model(request, obj, form, change)
        obj.update_obligation_counts()

    @beartype
    def status_chart(self, obj: Any) -> str:
        """Return an HTML representation of the status chart for the mechanism.

        Args:
            obj: EnvironmentalMechanism instance.

        Returns:
            HTML string for the status chart.

        """
        # Implementation for status_chart goes here.
        return ""  # Ensure all code paths return a string

    @staticmethod
    @beartype
    def has_add_permission(request: Any) -> bool:
        """Determine if the user has permission to add a mechanism in admin.

        Args:
            request: The HTTP request object.

        Returns:
            True if the user can add a mechanism, False otherwise.

        """
        # Implementation for has_add_permission goes here.
        return False  # Ensure all code paths return a bool

    @staticmethod
    @beartype
    def is_overdue(obj: EnvironmentalMechanism) -> bool:
        """Display whether an obligation is overdue.

        Args:
            obj: The EnvironmentalMechanism instance.

        Returns:
            True if overdue, False otherwise.

        """
        if obj.status == "completed":
            return False

        if not hasattr(obj, "action_due_date") or not obj.action_due_date:
            return False

        return obj.action_due_date < timezone.now().date()
