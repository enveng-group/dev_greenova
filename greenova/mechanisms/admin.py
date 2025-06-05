"""Admin configuration for the EnvironmentalMechanism model.

This module customizes the Django admin interface for the EnvironmentalMechanism model,
including optimized queryset, obligation count display, and status helpers.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from beartype import beartype
from django.contrib import admin
from django.utils import timezone

from .models import EnvironmentalMechanism
from .permissions import user_can_view_mechanism

if TYPE_CHECKING:
    from django.forms import ModelForm
    from django.http import HttpRequest


@admin.register(EnvironmentalMechanism)
class EnvironmentalMechanismAdmin(admin.ModelAdmin):
    """Admin configuration for EnvironmentalMechanism model."""

    list_display = (
        "name",
        "project",
        "overdue_count",
        "not_started_count",
        "in_progress_count",
        "completed_count",
        "get_total_obligations",
        "updated_at",
    )
    list_filter = ("project__name", "status", "updated_at")
    search_fields = ("name", "project__name")
    readonly_fields = (
        "updated_at",
        "overdue_count",
        "not_started_count",
        "in_progress_count",
        "completed_count",
        "status_chart",
    )
    ordering = ("name", "-updated_at")

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
    def get_queryset(self, request: "HttpRequest") -> Any:
        """Optimize queryset by prefetching related data.

        Args:
            request: The HTTP request object.

        Returns:
            Queryset with related project prefetched.
        """
        queryset = super().get_queryset(request)
        return cast("Any", queryset.select_related("project"))

    @staticmethod
    @beartype
    def get_total_obligations(obj: EnvironmentalMechanism) -> int:
        """Get total obligations count for the mechanism.

        Args:
            obj: The EnvironmentalMechanism instance.

        Returns:
            The total number of obligations.
        """
        return cast("int", obj.total_obligations)

    get_total_obligations.short_description = "Total"  # type: ignore

    @beartype
    def save_model(
        self,
        request: "HttpRequest",
        obj: EnvironmentalMechanism,
        form: "ModelForm",
        change: bool,
    ) -> None:
        """Update counts when saving model in admin.

        Args:
            request: The HTTP request object.
            obj: The EnvironmentalMechanism instance.
            form: The model form instance.
            change: Whether this is an update.

        Returns:
            None.
        """
        super().save_model(request, obj, form, change)
        obj.update_obligation_counts()

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
