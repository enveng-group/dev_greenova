"""
Admin configuration for the obligations app.

This module registers the Obligation model and related admin customizations
for environmental obligations management.
"""
import logging
from typing import ClassVar

from constants import (
    FREQUENCY_DISPLAY_NAMES,
)
from django import forms
from django.contrib import admin
from django.utils import timezone
from models import Obligation
from roles import get_responsibility_choices

logger = logging.getLogger(__name__)


class OverdueFilter(admin.SimpleListFilter):
    """Filter for overdue obligations."""

    title: ClassVar[str] = "Overdue Status"
    parameter_name: ClassVar[str] = "overdue_status"

    def lookups(self, request, model_admin):
        """Return filter options for overdue status."""
        return (
            ("overdue", "Overdue"),
            ("not_overdue", "Not Overdue"),
        )

    def queryset(self, request, queryset):
        """Filter queryset based on overdue status selection."""
        today = timezone.now().date()
        if self.value() == "overdue":
            return queryset.filter(action_due_date__lt=today).exclude(
                status="completed"
            )
        if self.value() == "not_overdue":
            return queryset.exclude(action_due_date__lt=today).exclude(
                status="completed"
            )
        return queryset


class ObligationAdminForm(forms.ModelForm):
    """Form for customizing obligation admin interface."""
    recurring_obligation = forms.BooleanField(
        required=True, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    # ...existing code...
    inspection = forms.BooleanField(
        required=False,  # Changed to False to make it non-mandatory
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    # ...existing code...
    inspection_frequency = forms.ChoiceField(
        choices=[
            ("", "---------")
        ] + [
            (v, v)
            for v in FREQUENCY_DISPLAY_NAMES.values()
        ],
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    # ...existing code...
    responsibility = forms.ChoiceField(
        choices=get_responsibility_choices(),
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        """Meta options for ObligationAdminForm."""
        model: ClassVar[type[Obligation]] = Obligation
        fields: ClassVar[list[str]] = [
            "recurring_obligation",
            "inspection",
            "inspection_frequency",
            "responsibility",
            "project",
            "primary_environmental_mechanism",
            "environmental_aspect",
            "obligation",
            "obligation_type",
            "action_due_date",
            "close_out_date",
            "status",
            "recurring_frequency",
            "recurring_status",
            "recurring_forcasted_date",
            "site_or_desktop",
            "accountability",
            "project_phase",
            "supporting_information",
            "general_comments",
            "compliance_comments",
            "non_conformance_comments",
        ]
    # ...existing code...
