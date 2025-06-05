"""Admin configuration for the Obligations app.

This module customizes the Django admin interface for the Obligation model,
including custom filters, inlines, and admin actions.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import logging
from typing import Any, Optional

from beartype import beartype
from auditing.models import ComplianceComment, NonConformanceComment
from core.utils.roles import get_responsibility_choices
from django import forms
from django.contrib import admin
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpRequest
from django.utils import timezone

from .models import Obligation, ObligationEvidence
from .utils import is_obligation_overdue
from .permissions import user_can_view_obligation

logger = logging.getLogger(__name__)


class ComplianceInline(admin.TabularInline):
    """Inline admin for compliance comments."""

    model = ComplianceComment
    extra = 1


class NonConformanceInline(admin.TabularInline):
    """Inline admin for non-conformance comments."""

    model = NonConformanceComment
    extra = 1


class OverdueFilter(admin.SimpleListFilter):
    """Filter for overdue obligations."""

    title = "Overdue Status"
    parameter_name = "overdue_status"

    @beartype
    def lookups(self, request: HttpRequest, model_admin: Any) -> tuple[tuple[str, str], ...]:
        """Return filter options for overdue status.

        Args:
            request: The HTTP request object.
            model_admin: The model admin instance.

        Returns:
            Tuple of filter options.
        """
        return (
            ("overdue", "Overdue"),
            ("not_overdue", "Not Overdue"),
        )

    @beartype
    def queryset(self, request: HttpRequest, queryset: QuerySet) -> Optional[QuerySet]:
        """Filter queryset based on overdue status.

        Args:
            request: The HTTP request object.
            queryset: The queryset to filter.

        Returns:
            Filtered queryset or None.
        """
        today = timezone.now().date()
        if self.value() == "overdue":
            return queryset.filter(action_due_date__lt=today).exclude(
                status="completed",
            )
        if self.value() == "not_overdue":
            return queryset.exclude(action_due_date__lt=today).exclude(
                status="completed",
            )
        return None


class ObligationAdminForm(forms.ModelForm):
    """Custom admin form for the Obligation model."""

    recurring_obligation = forms.BooleanField(
        required=True, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    inspection = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    inspection_frequency = forms.ChoiceField(
        choices=[
            ("", "---------"),
            ("Daily", "Daily"),
            ("Weekly", "Weekly"),
            ("Fortnightly", "Fortnightly"),
            ("Monthly", "Monthly"),
            ("Quarterly", "Quarterly"),
            ("Annually", "Annually"),
        ],
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    responsibility = forms.ChoiceField(
        choices=get_responsibility_choices(),
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Obligation
        exclude = ["obligation_number"]

    @beartype
    def save(self, commit: bool = True) -> Obligation:
        """Override save to ensure obligation_number and timestamps are set.

        Args:
            commit: Whether to commit the save.

        Returns:
            The saved Obligation instance.
        """
        instance = super().save(commit=False)
        if not instance.pk:
            instance.obligation_number = Obligation.get_next_obligation_number()
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
    fields = ["file", "description"]
    verbose_name = "Evidence File"
    verbose_name_plural = "Evidence Files"

    @beartype
    def get_formset(
        self, request: HttpRequest, obj: Optional[Obligation] = None, **kwargs: Any
    ) -> Any:
        """Show inline only when editing an existing obligation.

        Args:
            request: The HTTP request object.
            obj: The obligation instance (optional).
            **kwargs: Additional keyword arguments.

        Returns:
            The formset instance.
        """
        if obj is None:
            self.extra = 0
        else:
            self.extra = 1
        return super().get_formset(request, obj, **kwargs)


@admin.register(Obligation)
class ObligationAdmin(admin.ModelAdmin):
    """Admin configuration for obligations."""

    form = ObligationAdminForm
    inlines = [
        ObligationEvidenceInline,
        ComplianceInline,
        NonConformanceInline,
    ]

    list_display = [
        "obligation_number",
        "project",
        "primary_environmental_mechanism",
        "is_overdue",
        "status",
        "action_due_date",
    ]

    fieldsets = [
        (
            "Basic Information",
            {
                "fields": [
                    "project",
                    "primary_environmental_mechanism",
                    "environmental_aspect",
                    "obligation",
                    "obligation_type",
                ],
            },
        ),
        (
            "Dates and Status",
            {"fields": ["action_due_date", "close_out_date", "status"]},
        ),
        (
            "Recurring Details",
            {
                "fields": [
                    "recurring_obligation",
                    "recurring_frequency",
                    "recurring_status",
                    "recurring_forecasted_date",
                ],
            },
        ),
        (
            "Inspection Details",
            {"fields": ["inspection", "inspection_frequency", "site_or_desktop"]},
        ),
        (
            "Additional Information",
            {
                "fields": [
                    "accountability",
                    "responsibility",
                    "project_phase",
                    "supporting_information",
                    "general_comments",
                ],
            },
        ),
    ]

    list_filter = [
        OverdueFilter,
        "status",
        "primary_environmental_mechanism",
        "project_phase",
        "recurring_obligation",
    ]
    search_fields = [
        "obligation_number",
        "obligation",
        "project__name",
        "responsibility",
    ]
    date_hierarchy = "action_due_date"

    @admin.display(
        description="Overdue",
        boolean=True,
    )
    @beartype
    def is_overdue(self, obj: Obligation) -> bool:
        """Display whether an obligation is overdue.

        Args:
            obj: The obligation instance.

        Returns:
            True if overdue, False otherwise.
        """
        return is_obligation_overdue(obj)

    @beartype
    def get_queryset(self, request: HttpRequest) -> QuerySet[Obligation]:
        """Optimize queryset for admin view by pre-fetching related fields.

        Args:
            request: The HTTP request object.

        Returns:
            QuerySet: Optimized queryset with related fields.
        """
        qs = super().get_queryset(request)
        return qs.select_related("project", "primary_environmental_mechanism")

    @beartype
    def save_model(
        self, request: HttpRequest, obj: Obligation, form: ModelForm, change: bool,
    ) -> None:
        """Log obligation changes in admin and ensure proper obligation number.

        Args:
            request: The HTTP request object.
            obj: The obligation instance being saved.
            form: The model form instance.
            change: Boolean indicating if this is an update.

        Returns:
            None.
        """
        try:
            if not change and (
                not obj.obligation_number or obj.obligation_number.strip() == ""
            ):
                obj.obligation_number = Obligation.get_next_obligation_number()
            if not change and not obj.created_at:
                obj.created_at = timezone.now()
                obj.updated_at = timezone.now()
            action = "Updated" if change else "Created"
            logger.info(
                "%s obligation %s for project %s",
                action,
                obj.obligation_number,
                obj.project.name,
            )
            super().save_model(request, obj, form, change)
            if obj.primary_environmental_mechanism:
                obj.primary_environmental_mechanism.update_obligation_counts()
        except Exception as e:
            logger.exception("Error saving obligation: %s", e)
            raise

    actions = ["update_recurring_dates"]

    @admin.action(description="Update recurring forecasted dates")
    @beartype
    def update_recurring_dates(self, request: HttpRequest, queryset: QuerySet[Obligation]) -> None:
        """Update recurring forecasted dates for selected obligations.

        Args:
            request: The HTTP request object.
            queryset: The queryset of selected obligations.

        Returns:
            None.
        """
        count = 0
        for obligation in queryset:
            if obligation.update_recurring_forecasted_date():
                obligation.save()
                count += 1

        self.message_user(
            request, "Successfully updated %d recurring forecasted dates" % count,
        )

    @beartype
    def get_inlines(
        self, request: HttpRequest, obj: Optional[Obligation] = None
    ) -> list[Any]:
        """Only show inlines when editing an existing object.

        Args:
            request: The HTTP request object.
            obj: The obligation instance (optional).

        Returns:
            List of inlines to display.
        """
        if obj:
            return [ObligationEvidenceInline, ComplianceInline, NonConformanceInline]
        return []
