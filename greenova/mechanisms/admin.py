from django.contrib import admin
from django.utils.html import format_html
from .models import EnvironmentalMechanism, ChartConfiguration
from utils.mechanism_mapping import get_reverse_mapping

@admin.register(ChartConfiguration)
class ChartConfigurationAdmin(admin.ModelAdmin):
    """Admin interface for chart configurations."""

    list_display = ('mechanism', 'chart_type', 'display_order', 'is_active', 'updated_at')
    list_filter = ('chart_type', 'is_active')
    search_fields = ('mechanism__name',)
    ordering = ('display_order', 'created_at')


@admin.register(EnvironmentalMechanism)
class EnvironmentalMechanismAdmin(admin.ModelAdmin):
    """Admin interface for environmental mechanisms."""

    list_display = (
        'id',
        'name',
        'project',
        'not_started_count',
        'in_progress_count',
        'completed_count',
        'total_obligations',
        'status',
        'updated_at'
    )

    list_filter = ('project', 'chart_config__chart_type')
    search_fields = ('name', 'description', 'project__name')
    ordering = ('name', '-updated_at')

    def primary_mechanism_name(self, obj):
        """Display the original mechanism name."""
        # Use the shared reverse mapping
        reverse_mapping = get_reverse_mapping()
        return reverse_mapping.get(obj.name, obj.name)
    primary_mechanism_name.short_description = 'Primary Environmental Mechanism'
    primary_mechanism_name.admin_order_field = 'name'

    def total_obligations(self, obj):
        """Display total count of obligations."""
        return obj.not_started_count + obj.in_progress_count + obj.completed_count
    total_obligations.short_description = 'Total Obligations'

    def chart_type_display(self, obj):
        """Display chart type with color-coded formatting."""
        if hasattr(obj, 'chart_config'):
            chart_type = obj.chart_config.chart_type
            colors = {
                'polar': '#4CAF50',  # Green
                'bar': '#2196F3',    # Blue
                'pie': '#FFC107',    # Amber
                'doughnut': '#9C27B0'  # Purple
            }
            color = colors.get(chart_type, '#757575')  # Default gray
            return format_html(
                '<span style="color: {};">{}</span>',
                color,
                chart_type.title()
            )
        return '-'
    chart_type_display.short_description = 'Chart Type'
    chart_type_display.admin_order_field = 'chart_config__chart_type'
