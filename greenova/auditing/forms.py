# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Auditing forms for the auditing app.

This module provides Django forms for managing audits, audit entries,
mitigations, corrective actions, and comments, with strict type annotations
and runtime type checking.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Forms for audit, mitigation, corrective action, and comment management

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from beartype import beartype
from dal import autocomplete
from django import forms
from obligations.models import Obligation

from .models import (
    Audit,
    AuditEntry,
    ComplianceComment,
    CorrectiveAction,
    Mitigation,
    NonConformanceComment,
)


class MitigationForm(forms.ModelForm):
    """Form for creating and updating mitigations."""

    audit_entry = forms.ModelChoiceField(
        queryset=AuditEntry.objects.all(),
        widget=autocomplete.ModelSelect2(url="auditentry-autocomplete"),
    )

    class Meta:
        model = Mitigation
        fields = ["audit_entry", "description", "status"]
        # Optionally, you can set choices for status field here if needed
        # widgets = {"status": forms.Select(choices=MITIGATION_STATUS_CHOICES)}

    @beartype
    def __init__(self, *args, **kwargs) -> None:
        """Initialize the MitigationForm and set up the crispy form helper.

        Args:
            *args: Positional arguments for the parent constructor.
            **kwargs: Keyword arguments for the parent constructor.

        """
        super().__init__(*args, **kwargs)


class CorrectiveActionForm(forms.ModelForm):
    """Form for creating and updating corrective actions."""

    mitigation = forms.ModelChoiceField(
        queryset=Mitigation.objects.all(),
        widget=autocomplete.ModelSelect2(url="mitigation-autocomplete"),
    )
    assigned_to = forms.ModelChoiceField(
        queryset=forms.models.User.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2(url="user-autocomplete"),
    )

    class Meta:
        model = CorrectiveAction
        fields = ["mitigation", "task", "status", "assigned_to", "due_date"]
        # Optionally, you can set choices for status field here if needed
        # widgets = {"status": forms.Select(choices=CORRECTIVE_ACTION_STATUS_CHOICES)}

    @beartype
    def __init__(self, *args, **kwargs) -> None:
        """Initialize the CorrectiveActionForm and set up the crispy form helper.

        Args:
            *args: Positional arguments for the parent constructor.
            **kwargs: Keyword arguments for the parent constructor.

        """
        super().__init__(*args, **kwargs)


class AuditEntryForm(forms.ModelForm):
    """Form for creating and updating audit entries."""

    audit = forms.ModelChoiceField(
        queryset=Audit.objects.all(),
        widget=autocomplete.ModelSelect2(url="audit-autocomplete"),
    )
    obligation = forms.ModelChoiceField(
        queryset=Obligation.objects.all(),
        widget=autocomplete.ModelSelect2(url="obligation-autocomplete"),
    )

    class Meta:
        model = AuditEntry
        fields = ["audit", "obligation", "status", "finding"]

    @beartype
    def __init__(self, *args, **kwargs) -> None:
        """Initialize the AuditEntryForm and set up the crispy form helper.

        Args:
            *args: Positional arguments for the parent constructor.
            **kwargs: Keyword arguments for the parent constructor.

        """
        super().__init__(*args, **kwargs)


class ComplianceCommentForm(forms.ModelForm):
    """Form for adding compliance comments."""

    obligation = forms.ModelChoiceField(
        queryset=Obligation.objects.all(),
        widget=autocomplete.ModelSelect2(url="obligation-autocomplete"),
    )

    class Meta:
        model = ComplianceComment
        fields = ["obligation", "text"]

    @beartype
    def __init__(self, *args, **kwargs) -> None:
        """Initialize the ComplianceCommentForm and set up the crispy form helper.

        Args:
            *args: Positional arguments for the parent constructor.
            **kwargs: Keyword arguments for the parent constructor.

        """
        super().__init__(*args, **kwargs)


class NonConformanceCommentForm(forms.ModelForm):
    """Form for adding non-conformance comments."""

    obligation = forms.ModelChoiceField(
        queryset=Obligation.objects.all(),
        widget=autocomplete.ModelSelect2(url="obligation-autocomplete"),
    )

    class Meta:
        model = NonConformanceComment
        fields = ["obligation", "text"]

    @beartype
    def __init__(self, *args, **kwargs) -> None:
        """Initialize the NonConformanceCommentForm and set up the crispy form helper.

        Args:
            *args: Positional arguments for the parent constructor.
            **kwargs: Keyword arguments for the parent constructor.

        """
        super().__init__(*args, **kwargs)


# NOTE: You must implement the corresponding autocomplete views and urls for each ModelSelect2 widget above.
# See the django-autocomplete-light documentation for details.
