# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Forms for obligations management in the obligations app.

This module provides Django forms for creating, updating, filtering, and
uploading evidence for obligations, with strict type annotations and runtime
type checking.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Forms for obligations, responsibilities, evidence upload, and filtering

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging
from typing import Any

import bleach
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Fieldset, Layout, Row, Submit
from dal import autocomplete
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from mechanisms.models import EnvironmentalMechanism
from projects.models import Project
from responsibility.models import Responsibility, ResponsibilityAssignment

from .constants import (
    FREQUENCY_CHOICES,
    STATUS_CHOICES,
    STATUS_COMPLETED,
    STATUS_NOT_STARTED,
)
from .models import Obligation, ObligationEvidence
from .utils import normalize_frequency
from .types import ObligationDataDict

from beartype import beartype

User = get_user_model()

logger = logging.getLogger(__name__)

ResponsibilityAssignmentFormSet = inlineformset_factory(
    Obligation,
    ResponsibilityAssignment,
    fields=("user", "responsibility"),
    extra=1,
    can_delete=True,
)


class FilterForm(forms.Form):
    """Base form for filtering with GET method."""

    @beartype
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the FilterForm and set GET method for all fields."""
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["formmethod"] = "get"  # Ensure GET method is used

    @beartype
    def clean(self) -> dict[str, Any]:
        """Override clean to handle cleaned data appropriately.

        Returns:
            The cleaned data dictionary.
        """
        return super().clean()
        # Add any additional validation or transformation logic here


class ObligationForm(forms.ModelForm):
    """Form for creating and updating obligations."""

    # ... field definitions unchanged ...

    @beartype
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the ObligationForm with project and user context.

        Args:
            *args: Positional arguments for the parent constructor.
            **kwargs: Keyword arguments for the parent constructor.
        """
        self.project = kwargs.pop("project", None)
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Obligation Details",
                Row(
                    Column("obligation_number", css_class="col-md-4"),
                    Column("project", css_class="col-md-4"),
                    Column("primary_environmental_mechanism", css_class="col-md-4"),
                ),
                Row(
                    Column("environmental_aspect", css_class="col-md-6"),
                    Column("custom_environmental_aspect", css_class="col-md-6"),
                ),
                "obligation",
                "procedure",
                "obligation_type",
                Row(
                    Column("action_due_date", css_class="col-md-6"),
                    Column("close_out_date", css_class="col-md-6"),
                ),
                "status",
            ),
            Fieldset(
                "Recurring Details",
                "recurring_obligation",
                "recurring_frequency",
                "recurring_status",
                "recurring_forecasted_date",
            ),
            Fieldset(
                "Inspection Details",
                "inspection",
                "inspection_frequency",
                "site_or_desktop",
            ),
            Fieldset(
                "Additional Information",
                "accountability",
                "project_phase",
                "supporting_information",
                "general_comments",
                "compliance_comments",
                "non_conformance_comments",
                "evidence_notes",
                "new_control_action_required",
                "gap_analysis",
                "notes_for_gap_analysis",
                "covered_in_which_inspection_checklist",
            ),
            Submit("submit", "Save Obligation", css_class="btn btn-primary"),
        )

        if self.project:
            self.fields["project"].initial = self.project
            self.fields["project"].widget = forms.HiddenInput()
            self.fields[
                "primary_environmental_mechanism"
            ].queryset = EnvironmentalMechanism.objects.filter(project=self.project)

        instance = kwargs.get("instance")
        if instance:
            self.fields["obligation_number"].widget.attrs["readonly"] = True
            self.fields[
                "obligation_number"
            ].help_text = "Obligation ID cannot be changed"
            self.fields["obligation_number"].initial = instance.obligation_number

            for field_name in [
                "recurring_obligation",
                "inspection",
                "new_control_action_required",
                "gap_analysis",
            ]:
                if hasattr(instance, field_name):
                    self.fields[field_name].initial = getattr(instance, field_name)

            if instance.environmental_aspect == "Other":
                self.fields[
                    "custom_environmental_aspect"
                ].initial = instance.custom_environmental_aspect
        else:
            self.fields[
                "obligation_number"
            ].help_text = (
                "Unique identifier (PCEMP-XXX format). Leave blank to auto-generate."
            )

        help_texts = {
            "obligation_number": "Unique identifier for this obligation",
            "environmental_aspect": 'Select an environmental aspect or "Other" to specify a custom aspect',
            "custom_environmental_aspect": 'Required if Environmental Aspect is "Other"',
            "action_due_date": "When this obligation needs to be fulfilled",
            "recurring_obligation": "Does this obligation repeat on a regular schedule?",
            "recurring_frequency": "How often this obligation repeats",
            "inspection": "Is an inspection required for this obligation?",
            "evidence_notes": "Notes about uploaded evidence files",
        }

        for field, text in help_texts.items():
            if field in self.fields:
                self.fields[field].help_text = text

    @beartype
    def clean_obligation_number(self) -> str | None:
        """Validate and format obligation number if provided.

        Returns:
            The validated obligation number or None.

        Raises:
            ValidationError: If the format is invalid or duplicate exists.
        """
        obligation_number = self.cleaned_data.get("obligation_number")

        if self.instance and self.instance.pk:
            return obligation_number

        if obligation_number:
            import re

            if not re.match(r"^PCEMP-\d+$", obligation_number):
                if obligation_number.isdigit():
                    return f"PCEMP-{obligation_number}"
                if "-" in obligation_number:
                    parts = obligation_number.split("-", 1)
                    if len(parts) > 1 and parts[1].isdigit():
                        return f"PCEMP-{parts[1]}"
                msg = (
                    "Obligation number must be in the format PCEMP-XXX where XXX is a number."
                )
                raise ValidationError(msg)

            existing = Obligation.objects.filter(obligation_number=obligation_number)
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                msg = f"An obligation with number {obligation_number} already exists."
                raise ValidationError(msg)

        return obligation_number

    @beartype
    def clean_recurring_frequency(self) -> str:
        """Normalize recurring frequency if provided.

        Returns:
            The normalized frequency string.

        Raises:
            ValidationError: If frequency is required but missing.
        """
        frequency = self.cleaned_data.get("recurring_frequency")
        recurring = self.cleaned_data.get("recurring_obligation")

        if recurring and not frequency:
            msg = "Frequency is required for recurring obligations"
            raise ValidationError(msg)

        if not recurring:
            return ""

        return normalize_frequency(frequency)

    @beartype
    def clean_custom_environmental_aspect(self) -> str:
        """Validate custom aspect is provided when needed.

        Returns:
            The custom environmental aspect string.

        Raises:
            ValidationError: If required but not provided.
        """
        aspect = self.cleaned_data.get("environmental_aspect")
        custom_aspect = self.cleaned_data.get("custom_environmental_aspect")

        if aspect == "Other" and not custom_aspect:
            msg = "Please specify a custom environmental aspect."
            raise ValidationError(msg)

        return custom_aspect

    @beartype
    def clean_obligation(self) -> str:
        """Sanitize the obligation field using bleach.

        Returns:
            The cleaned obligation string.
        """
        value = self.cleaned_data.get("obligation", "")
        return bleach.clean(value)

    @beartype
    def clean_supporting_information(self) -> str:
        """Sanitize the supporting_information field using bleach.

        Returns:
            The cleaned supporting information string.
        """
        value = self.cleaned_data.get("supporting_information", "")
        return bleach.clean(value)

    @beartype
    def clean(self) -> dict[str, Any]:
        """Cross-field validation to enforce business rules.

        Returns:
            The cleaned data dictionary.
        """
        cleaned_data = super().clean()

        action_due_date = cleaned_data.get("action_due_date")
        close_out_date = cleaned_data.get("close_out_date")
        status = cleaned_data.get("status")

        if close_out_date and action_due_date and close_out_date < action_due_date:
            self.add_error(
                "close_out_date",
                "Close out date must be after action due date",
            )

        if status == STATUS_COMPLETED and not close_out_date:
            self.add_error(
                "close_out_date",
                "Close out date is required when status is completed",
            )

        recurring = cleaned_data.get("recurring_obligation")
        if recurring:
            for field in ["recurring_frequency", "recurring_status"]:
                if not cleaned_data.get(field):
                    self.add_error(
                        field,
                        f"{field.replace('_', ' ').title()} is required for recurring obligations",
                    )

        inspection = cleaned_data.get("inspection")
        if inspection:
            for field in ["inspection_frequency", "site_or_desktop"]:
                if not cleaned_data.get(field):
                    self.add_error(
                        field,
                        f"{field.replace('_', ' ').title()} is required when inspection is enabled",
                    )

        gap_analysis = cleaned_data.get("gap_analysis")
        if gap_analysis and not cleaned_data.get("notes_for_gap_analysis"):
            self.add_error(
                "notes_for_gap_analysis",
                "Notes are required when gap analysis is enabled",
            )

        return cleaned_data

    @beartype
    def save(self, commit: bool = True) -> Obligation:
        """Override save to ensure obligation_number is set for new instances.

        Args:
            commit: Whether to commit changes to the database.

        Returns:
            The saved Obligation instance.
        """
        instance = super().save(commit=False)

        if not instance.pk and not instance.obligation_number:
            instance.obligation_number = Obligation.get_next_obligation_number()

        if instance.environmental_aspect == "Other":
            instance.custom_environmental_aspect = self.cleaned_data.get(
                "custom_environmental_aspect",
                "",
            )

        if instance.recurring_obligation and not instance.recurring_forecasted_date:
            instance.update_recurring_forecasted_date()

        if commit:
            instance.save()
            self.save_m2m()

        return instance

    class Meta:
        model = Obligation
        fields = "__all__"
        exclude = [
            "person_email",
        ]
        widgets = {
            "obligation": forms.Textarea(attrs={"rows": 4}),
            "supporting_information": forms.Textarea(attrs={"rows": 3}),
            "general_comments": forms.Textarea(attrs={"rows": 3}),
            "compliance_comments": forms.Textarea(attrs={"rows": 3}),
            "non_conformance_comments": forms.Textarea(attrs={"rows": 3}),
            "evidence_notes": forms.Textarea(attrs={"rows": 2}),
            "notes_for_gap_analysis": forms.Textarea(attrs={"rows": 3}),
            "action_due_date": forms.DateInput(attrs={"type": "date"}),
            "close_out_date": forms.DateInput(attrs={"type": "date"}),
            "recurring_forecasted_date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "primary_environmental_mechanism": "Environmental Mechanism",
            "action_due_date": "Due Date",
            "recurring_forecasted_date": "Next Forecasted Due Date",
        }
        help_texts = {
            "environmental_aspect": "Select the environmental aspect this obligation relates to",
            "custom_environmental_aspect": 'If "Other" is selected above, please specify the aspect',
            "obligation": "Describe the specific obligation requirement",
            "recurring_obligation": "Does this obligation recur on a regular schedule?",
            "inspection": "Does this obligation require inspections?",
            "gap_analysis": "Is a gap analysis required for this obligation?",
        }


class ResponsibilityAssignmentForm(forms.Form):
    """Form for assigning responsibilities to users."""

    user = forms.ModelChoiceField(queryset=User.objects.all(), label="User")
    responsibility = forms.ModelChoiceField(
        queryset=Responsibility.objects.all(),
        label="Responsibility Role",
    )


class ObligationResponsibilityForm(forms.Form):
    """Form for selecting responsibility assignments."""

    assignments = forms.ModelMultipleChoiceField(
        queryset=ResponsibilityAssignment.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Assigned Users and Roles",
    )


class EvidenceUploadForm(forms.ModelForm):
    """Form for uploading evidence files."""

    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "form-input",
                "accept": ".pdf,.doc,.docx,.xls,.xlsx,.png,.jpg,.jpeg,.gif,.txt,.csv",
            },
        ),
        help_text="Upload evidence files (max 25MB). Allowed formats: PDF, DOC, DOCX, XLS, XLSX, PNG, JPG, JPEG, GIF, TXT, CSV",
    )

    description = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Brief description of the evidence file",
            },
        ),
    )

    @beartype
    def clean_file(self) -> Any:
        """Validate file size and extension.

        Returns:
            The validated file.

        Raises:
            ValidationError: If file is too large, wrong type, or too many files.
        """
        file = self.cleaned_data.get("file")
        if file:
            if file.size > 26214400:
                msg = "File size must be under 25MB"
                raise ValidationError(msg)

            allowed_extensions = [
                "pdf",
                "doc",
                "docx",
                "xls",
                "xlsx",
                "png",
                "jpg",
                "jpeg",
                "gif",
                "txt",
                "csv",
            ]

            file_ext = file.name.split(".")[-1].lower()
            if file_ext not in allowed_extensions:
                msg = (
                    f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
                )
                raise ValidationError(msg)

            if (
                self.instance
                and self.instance.obligation
                and (
                    ObligationEvidence.objects.filter(
                        obligation=self.instance.obligation,
                    ).count()
                    >= 5
                )
            ):
                msg = "Maximum of 5 evidence files allowed per obligation"
                raise ValidationError(msg)

        return file

    class Meta:
        model = ObligationEvidence
        fields = ["file", "description"]
        widgets = {
            "description": forms.TextInput(
                attrs={"placeholder": "Brief description of the file"},
            ),
        }


class ObligationFilterForm(forms.Form):
    """Form for filtering obligations."""

    search = forms.CharField(
        required=False,
        max_length=100,
        label="Search",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search...",
                "class": "form-input",
            },
        ),
    )
    status = forms.ChoiceField(
        required=False,
        choices=[("", "All"), ("open", "Open"), ("closed", "Closed")],
        label="Status",
        widget=forms.Select(attrs={"class": "form-input"}),
    )
    phase = forms.ChoiceField(
        required=False,
        choices=[("", "All"), ("planning", "Planning"), ("execution", "Execution")],
        label="Phase",
        widget=forms.Select(attrs={"class": "form-input"}),
    )
    sort = forms.ChoiceField(
        required=False,
        choices=[("", "Default"), ("name", "Name"), ("status", "Status")],
        label="Sort By",
        widget=forms.Select(attrs={"class": "form-input"}),
    )
