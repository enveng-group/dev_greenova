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

"""Admin configuration for the obligations app.

This module registers the Obligation model and related admin customizations
for environmental obligations management.
"""
from roles import get_responsibility_choices
from models import Obligation
from django.utils import timezone
from django.contrib import admin
from django import forms
from constants import (
    FREQUENCY_DISPLAY_NAMES,
)
import logging
from typing import ClassVar


logger = logging.getLogger(__name__)


class OverdueFilter(admin.SimpleListFilter):
    """Filter for overdue obligations."""

    title: ClassVar[str] = "Overdue Status"
    parameter_name: ClassVar[str] = "overdue_status"

    def lookups(self, request: HttpRequest) -> tuple:
        """Return filter options for overdue status."""
        return (
            ("overdue", "Overdue"),
            ("not_overdue", "Not Overdue"),
        )

    def queryset(self, request: HttpRequest, queryset: QuerySet[Any]) -> QuerySet[Any]:
        """Filter queryset based on overdue status selection."""
        today = timezone.now().date()
        if self.value() == "overdue":
            return queryset.filter(action_due_date__lt=today).exclude(
                status="completed",
            )
        if self.value() == "not_overdue":
            return queryset.exclude(action_due_date__lt=today).exclude(
                status="completed",
            )
        return queryset


class ObligationAdminForm(forms.ModelForm):
    """Form for customizing obligation admin interface."""

    recurring_obligation = forms.BooleanField(
        required=True, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    # ...existing code...
    inspection = forms.BooleanField(
        required=False,  # Changed to False to make it non-mandatory
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    # ...existing code...
    inspection_frequency = forms.ChoiceField(
        choices=[
            ("", "---------"),
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
            "recurring_forecasted_date",
            "site_or_desktop",
            "accountability",
            "project_phase",
            "supporting_information",
            "general_comments",
            "compliance_comments",
            "non_conformance_comments",
        ]
    # ...existing code...
