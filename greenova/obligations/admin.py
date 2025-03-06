from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from django.forms import ModelForm
from django.utils import timezone
from .models import Obligation
from .utils import is_obligation_overdue
import logging

logger = logging.getLogger(__name__)

class OverdueFilter(admin.SimpleListFilter):
    """Filter for overdue obligations."""
    title = 'Overdue Status'
    parameter_name = 'overdue_status'

    def lookups(self, request, model_admin):
        return (
            ('overdue', 'Overdue'),
            ('not_overdue', 'Not Overdue'),
        )

    def queryset(self, request, queryset):
        today = timezone.now().date()
        if self.value() == 'overdue':
            return queryset.filter(
                action_due_date__lt=today
            ).exclude(status='completed')
        if self.value() == 'not_overdue':
            return queryset.exclude(
                action_due_date__lt=today
            ).exclude(status='completed')

@admin.register(Obligation)
class ObligationAdmin(admin.ModelAdmin):
    """Admin configuration for obligations."""
    list_display = [
        'obligation_number',
        'project',
        'primary_environmental_mechanism',
        'is_overdue',
        'status',
        'action_due_date'
    ]

    # Add fieldsets to organize the form better
    fieldsets = [
        ('Basic Information', {
            'fields': ['obligation_number', 'project', 'primary_environmental_mechanism',
                      'environmental_aspect', 'obligation', 'obligation_type']
        }),
        ('Dates and Status', {
            'fields': ['action_due_date', 'close_out_date', 'status']
        }),
        ('Recurring Details', {
            'fields': ['recurring_obligation', 'recurring_frequency',
                      'recurring_status', 'recurring_forcasted_date']
        }),
        ('Inspection Details', {
            'fields': ['inspection', 'inspection_frequency', 'site_or_desktop']
        }),
        ('Additional Information', {
            'fields': ['accountability', 'responsibility', 'project_phase',
                      'supporting_information', 'general_comments',
                      'compliance_comments', 'non_conformance_comments']
        })
    ]

    list_filter = [
        OverdueFilter,
        'status',
        'primary_environmental_mechanism',
        'project_phase',
        'recurring_obligation'
    ]
    search_fields = ['obligation_number', 'obligation', 'project__name']
    date_hierarchy = 'action_due_date'

    def is_overdue(self, obj):
        """Display whether an obligation is overdue."""
        return is_obligation_overdue(obj)

    is_overdue.short_description = 'Overdue'
    is_overdue.boolean = True

    def get_queryset(self, request: HttpRequest) -> QuerySet[Obligation]:
        """
        Optimize queryset for admin view by pre-fetching related fields.

        Args:
            request: The HTTP request object

        Returns:
            QuerySet: Optimized queryset with related fields
        """
        qs = super().get_queryset(request)
        return qs.select_related('project', 'primary_environmental_mechanism')

    def save_model(
            self,
            request: HttpRequest,
            obj: Obligation,
            form: ModelForm,
            change: bool) -> None:
        """
        Log obligation changes in admin and ensure proper obligation number.

        Args:
            request: The HTTP request object
            obj: The obligation instance being saved
            form: The model form instance
            change: Boolean indicating if this is an update
        """
        try:
            # For new obligations without a number, generate one
            if not change and (not obj.obligation_number or obj.obligation_number.strip() == ''):
                obj.obligation_number = Obligation.get_next_obligation_number()

            action = "Updated" if change else "Created"
            logger.info(
                f"{action} obligation {obj.obligation_number} "
                f"for project {obj.project.name}"
            )
            super().save_model(request, obj, form, change)

            # Update mechanism counts
            if obj.primary_environmental_mechanism:
                obj.primary_environmental_mechanism.update_obligation_counts()
        except Exception as e:
            logger.error(f"Error saving obligation: {str(e)}")
            raise

    actions = ['update_recurring_dates']

    def update_recurring_dates(self, request, queryset):
        """Update recurring forecasted dates for selected obligations."""
        count = 0
        for obligation in queryset:
            if obligation.update_recurring_forecasted_date():
                obligation.save()
                count += 1

        self.message_user(
            request,
            f"Successfully updated {count} recurring forecasted dates"
        )
    update_recurring_dates.short_description = "Update recurring forecasted dates"
