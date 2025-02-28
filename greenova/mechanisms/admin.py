from django.contrib import admin
from typing import Any
from django.http import HttpRequest
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
                       'in_progress_count', 'completed_count')
    ordering = ('name', '-updated_at')

    def get_queryset(self, request: HttpRequest) -> Any:
        """Optimize queryset by prefetching related data."""
        return super().get_queryset(request).select_related('project')

    def get_total_obligations(self, obj: EnvironmentalMechanism) -> int:
        """Get total obligations count."""
        return obj.total_obligations
    get_total_obligations.short_description = 'Total'  # type: ignore

    def save_model(self, request, obj, form, change):
        """Update counts when saving model in admin."""
        super().save_model(request, obj, form, change)
        obj.update_obligation_counts()
