from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from django.forms import ModelForm
from django.utils import timezone
from .models import Obligation, ObligationEvidence
from .utils import is_obligation_overdue
import logging
from django import forms

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

class ObligationAdminForm(forms.ModelForm):
    # Make recurring_obligation required but inspection optional
    recurring_obligation = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    inspection = forms.BooleanField(
        required=False,  # Changed to False to make it non-mandatory
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # Add this to ensure inspection_frequency is also not required
    inspection_frequency = forms.ChoiceField(
        choices=[('', '---------')] + [
            ('Daily', 'Daily'),
            ('Weekly', 'Weekly'),
            ('Fortnightly', 'Fortnightly'),
            ('Monthly', 'Monthly'),
            ('Quarterly', 'Quarterly'),
            ('Annually', 'Annually'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Obligation
        exclude = ['obligation_number']  # Exclude from form but handle in save

    def save(self, commit=True):
        """Override save to ensure obligation_number is set before validation."""
        instance = super().save(commit=False)

        # For new instances, generate obligation number and ensure datetime fields are set
        if not instance.pk:
            instance.obligation_number = Obligation.get_next_obligation_number()
            # Explicitly set created_at and updated_at for new instances to fix the NOT NULL constraint
            if not instance.created_at:
                instance.created_at = timezone.now()
            if not instance.updated_at:
                instance.updated_at = timezone.now()

        if commit:
            instance.save()
        return instance

class ObligationEvidenceInline(admin.TabularInline):
    """Inline admin for obligation evidence files."""
    model = ObligationEvidence
    extra = 1
    fields = ['file', 'description']
    verbose_name = "Evidence File"
    verbose_name_plural = "Evidence Files"

    def get_formset(self, request, obj=None, **kwargs):
        """Only show inline when editing an existing obligation (not during creation)."""
        if obj is None:
            self.extra = 0  # No empty forms when creating a new obligation
        else:
            self.extra = 1  # Show one empty form when editing
        return super().get_formset(request, obj, **kwargs)

@admin.register(Obligation)
class ObligationAdmin(admin.ModelAdmin):
    """Admin configuration for obligations."""
    form = ObligationAdminForm  # Use our custom form
    inlines = [ObligationEvidenceInline]

    list_display = [
        'obligation_number',
        'project',
        'primary_environmental_mechanism',
        'is_overdue',
        'status',
        'action_due_date'
    ]

    # Modified fieldsets - no need to include obligation_number here
    fieldsets = [
        ('Basic Information', {
            'fields': ['project', 'primary_environmental_mechanism',
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

    # No need for explicit exclude since we're using a custom form

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

            # Ensure created_at and updated_at are set for new objects
            if not change and not obj.created_at:
                obj.created_at = timezone.now()
                obj.updated_at = timezone.now()

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

    def get_inlines(self, request, obj=None):
        """Only show inlines when editing an existing object."""
        if obj:  # Only for existing obligations
            return [ObligationEvidenceInline]
        return []  # No inlines when creating a new obligation
