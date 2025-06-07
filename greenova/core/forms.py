"""Forms for the Greenova core app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from beartype import beartype
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser, EnvironmentalObligation, UserProfile


@beartype
class EnvironmentalObligationForm(forms.ModelForm):  # type: ignore[misc]
    """Form for creating and updating EnvironmentalObligation objects.

    Uses django-bootstrap5 for rendering.
    """

    class Meta:
        model = EnvironmentalObligation
        fields = ["name", "description", "due_date", "is_complete"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }


@beartype
class CustomUserCreationForm(UserCreationForm):  # type: ignore[misc]
    """Form for creating a new CustomUser (registration).

    Uses django-bootstrap5 for rendering.
    """

    class Meta:
        model = CustomUser
        fields = ("username", "email", "company", "is_mfa_enabled")


@beartype
class CustomUserChangeForm(UserChangeForm):  # type: ignore[misc]
    """Form for updating an existing CustomUser (admin/user profile).

    Uses django-bootstrap5 for rendering.
    """

    class Meta:
        model = CustomUser
        fields = ("username", "email", "company", "is_mfa_enabled")


@beartype
class UserProfileForm(forms.ModelForm):  # type: ignore[misc]
    """Form for editing a user's profile information.

    Uses django-bootstrap5 for rendering.
    """

    class Meta:
        model = UserProfile
        fields = ("display_name", "avatar", "preferences")
        widgets = {
            "preferences": forms.Textarea(attrs={"rows": 3}),
        }


@beartype
class AuditLogFilterForm(forms.Form):
    """Form for filtering audit log entries in the audit log view.

    Uses django-bootstrap5 for rendering.
    """

    user = forms.CharField(
        required=False,
        label="User",
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )
    action = forms.CharField(
        required=False,
        label="Action",
        widget=forms.TextInput(attrs={"placeholder": "Action"}),
    )
    object_type = forms.CharField(
        required=False,
        label="Object Type",
        widget=forms.TextInput(attrs={"placeholder": "Type"}),
    )
    date_from = forms.DateField(
        required=False,
        label="From Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    date_to = forms.DateField(
        required=False,
        label="To Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
