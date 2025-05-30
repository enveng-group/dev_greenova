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

"""Admin configuration for the mechanisms app.

This module registers the EnvironmentalMechanism model with the Django admin
and customizes its display and behavior for environmental professionals.
"""


from __future__ import annotations
from typing import TYPE_CHECKING, cast

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

    # Explicitly define fields to control their order in the admin form
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

    def get_queryset(self, request: HttpRequest) -> models.QuerySet:
        """Optimize queryset by prefetching related data."""
        queryset = super().get_queryset(request)
        return queryset.select_related("project")

    @staticmethod
    def get_total_obligations(obj: EnvironmentalMechanism) -> int:
        """Get total obligations count."""
        return cast("int", obj.total_obligations)

    # Add short description for admin list display
    get_total_obligations.short_description = "Total"  # type: ignore

    def save_model(
        self,
        request: HttpRequest,
        obj: EnvironmentalMechanism,
        form: ModelForm,
        change: bool,
    ) -> None:
        """Update counts when saving model in admin."""
        super().save_model(request, obj, form, change)
        obj.update_obligation_counts()

    @staticmethod
    def is_overdue(obj: EnvironmentalMechanism) -> bool:
        """Display whether an obligation is overdue."""
        if obj.status == "completed":
            return False

        if not hasattr(obj, "action_due_date") or not obj.action_due_date:
            return False

        return obj.action_due_date < timezone.now().date()
