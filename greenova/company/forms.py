# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Forms for company management in the company app.

This module provides Django forms for creating, updating, searching, and
managing companies, memberships, and documents, with strict type annotations
and runtime type checking.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Forms for company, membership, document, and user management

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from beartype import beartype
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Fieldset, Layout, Row, Submit
from dal import autocomplete
from django import forms
from django.contrib.auth import get_user_model

from .models import Company, CompanyDocument, CompanyMembership
from .types import CompanyProfileDict, EmployeeRecordDict

User = get_user_model()


class CompanyForm(forms.ModelForm):
    """Form for creating and updating companies."""

    class Meta:
        model = Company
        fields = [
            "name",
            "logo",
            "description",
            "website",
            "address",
            "phone",
            "email",
            "company_type",
            "size",
            "industry",
            "is_active",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "address": forms.Textarea(attrs={"rows": 3}),
            # Example: "company_type": forms.Select(choices=COMPANY_TYPE_CHOICES)
        }

    @beartype
    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the CompanyForm and set up the crispy form helper.

        Args:
            *args: Positional arguments for the parent constructor.
            **kwargs: Keyword arguments for the parent constructor.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Company Details",
                Row(
                    Column("name", css_class="form-group col-md-6 mb-0"),
                    Column("logo", css_class="form-group col-md-6 mb-0"),
                ),
                "description",
                "website",
                "address",
                "phone",
                "email",
                "company_type",
                "size",
                "industry",
                "is_active",
            ),
            Submit("submit", "Save Company"),
        )


class CompanyMembershipForm(forms.ModelForm):
    """Form for managing company memberships."""

    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(url="user-autocomplete"),
    )
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        widget=autocomplete.ModelSelect2(url="company-autocomplete"),
    )

    class Meta:
        model = CompanyMembership
        fields = ["company", "user", "role", "department", "position", "is_primary"]
        # Example: widgets = {"role": forms.Select(choices=COMPANY_ROLE_CHOICES)}

    @beartype
    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the CompanyMembershipForm and set up the crispy form helper.

        Args:
            *args: Positional arguments for the parent constructor.
            **kwargs: Keyword arguments for the parent constructor.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Membership Details",
                "company",
                "user",
                "role",
                "department",
                "position",
                "is_primary",
            ),
            Submit("submit", "Save Membership"),
        )


class CompanyDocumentForm(forms.ModelForm):
    """Form for uploading company documents."""

    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        widget=autocomplete.ModelSelect2(url="company-autocomplete"),
    )

    class Meta:
        model = CompanyDocument
        fields = ["company", "name", "description", "file", "document_type"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    @beartype
    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the CompanyDocumentForm and set up the crispy form helper.

        Args:
            *args: Positional arguments for the parent constructor.
            **kwargs: Keyword arguments for the parent constructor.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Document Details",
                "company",
                "name",
                "description",
                "file",
                "document_type",
            ),
            Submit("submit", "Upload Document"),
        )


class CompanySearchForm(forms.Form):
    """Form for searching companies."""

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name or description",
                "class": "form-input",
                "hx-get": "/company/search/",
                "hx-trigger": "keyup changed delay:500ms",
                "hx-target": "#company-list-container",
            },
        ),
    )
    company_type = forms.ChoiceField(
        required=False,
        choices=[("", "All Types"), *Company.COMPANY_TYPES],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "hx-get": "/company/search/",
                "hx-trigger": "change",
                "hx-target": "#company-list-container",
            },
        ),
    )
    industry = forms.ChoiceField(
        required=False,
        choices=[("", "All Industries"), *Company.INDUSTRY_SECTORS],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "hx-get": "/company/search/",
                "hx-trigger": "change",
                "hx-target": "#company-list-container",
            },
        ),
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={
                "hx-get": "/company/search/",
                "hx-trigger": "change",
                "hx-target": "#company-list-container",
            },
        ),
    )


class AddUserToCompanyForm(forms.Form):
    """Form for adding users to a company."""

    user = forms.ModelChoiceField(
        queryset=User.objects.all().order_by("username"),
        widget=autocomplete.ModelSelect2(url="user-autocomplete"),
    )
    role = forms.ChoiceField(
        choices=CompanyMembership.ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    department = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )
    position = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )
    is_primary = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={"class": "form-checkbox"}),
    )
