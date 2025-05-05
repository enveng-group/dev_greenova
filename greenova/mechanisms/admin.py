from __future__ import annotations

from typing import Any, cast

from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from django.utils import timezone

from .models import EnvironmentalMechanism


@admin.register(EnvironmentalMechanism)
class EnvironmentalMechanismAdmin(admin.ModelAdmin):
    """Admin configuration for EnvironmentalMechanism model."""
    list_display = (
        'name',
        'project',
        'overdue_count',
        'not_started_count',
        'in_progress_count',
        'completed_count',
        'get_total_obligations',
        'updated_at'
    )
    list_filter = ('project__name', 'status', 'updated_at')
    search_fields = ('name', 'project__name')
    readonly_fields = ('updated_at', 'overdue_count', 'not_started_count',
                       'in_progress_count', 'completed_count', 'status_chart')
    ordering = ('name', '-updated_at')

    # Explicitly define fields to control their order in the admin form
    fields = (
        'name', 'project', 'description', 'category', 'reference_number',
        'effective_date', 'status', 'primary_environmental_mechanism',
        'updated_at', 'overdue_count', 'not_started_count',
        'in_progress_count', 'completed_count'
    )

    def get_queryset(self, request: HttpRequest) -> Any:
        """Optimize queryset by prefetching related data."""
        queryset = super().get_queryset(request)
        return cast(Any, queryset.select_related('project'))

    @staticmethod
    def get_total_obligations(obj: EnvironmentalMechanism) -> int:
        """Get total obligations count."""
        return cast(int, obj.total_obligations)

    # Add short description for admin list display
    get_total_obligations.short_description = 'Total'  # type: ignore

    def save_model(
            self,
            request: HttpRequest,
            obj: EnvironmentalMechanism,
            form: ModelForm,
            change: bool
    ) -> None:
        """Update counts when saving model in admin."""
        super().save_model(request, obj, form, change)
        obj.update_obligation_counts()

    @staticmethod
    def is_overdue(obj: EnvironmentalMechanism) -> bool:
        """Display whether an obligation is overdue."""
        if obj.status == 'completed':
            return False

        if not hasattr(obj, 'action_due_date') or not obj.action_due_date:
            return False

        return obj.action_due_date < timezone.now().date()
