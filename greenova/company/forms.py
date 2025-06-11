import logging

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Company, CompanyDocument, CompanyMembership

logger = logging.getLogger(__name__)
User = get_user_model()


class CompanyForm(forms.ModelForm):
    """Form for creating and updating companies.

    This form provides fields for all company attributes with appropriate
    widgets for better user experience.
    """

    def clean(self):
        """Validate form data."""
        cleaned_data = super().clean()
        logger.info("Cleaning company form data: %s", cleaned_data)
        return cleaned_data

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
        }
        labels = {
            "name": _("Company Name"),
            "is_active": _("Active Status"),
        }
        help_texts = {
            "name": _("Enter a unique name for the company"),
            "company_type": _("Select the type that best describes this company"),
            "industry": _("Select the primary industry sector for this company"),
        }


class CompanyMembershipForm(forms.ModelForm):
    """Form for managing company memberships.

    This form allows adding users to companies with specific roles
    and department information.
    """

    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
        label=_("User"),
        help_text=_("Select a user to add to this company"),
    )

    class Meta:
        model = CompanyMembership
        fields = ["user", "role", "department", "position", "is_primary"]
        labels = {
            "role": _("Role in Company"),
            "is_primary": _("Primary Company"),
        }
        help_texts = {
            "role": _("Determines user permissions within this company"),
            "is_primary": _("Set if this is the user's main company"),
        }


class CompanyDocumentForm(forms.ModelForm):
    """Form for uploading company documents.

    This form handles document uploads with metadata like name,
    description, and document type.
    """

    class Meta:
        model = CompanyDocument
        fields = ["name", "description", "file", "document_type"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "name": _("Document Name"),
            "document_type": _("Document Type"),
        }
        help_texts = {
            "file": _("Upload a document file (PDF, DOC, XLS, etc.)"),
            "document_type": _("Categorize the document for easier retrieval"),
        }


class CompanySearchForm(forms.Form):
    """Form for searching and filtering companies.

    This form includes search and filter fields for company list view.
    """

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Search by name or description"),
                "class": "form-input",
            }
        ),
        label=_("Search"),
    )
    company_type = forms.ChoiceField(
        required=False,
        choices=[("", _("All Types")), *Company.COMPANY_TYPES],
        widget=forms.Select(attrs={"class": "form-select"}),
        label=_("Company Type"),
    )
    industry = forms.ChoiceField(
        required=False,
        choices=[("", _("All Industries")), *Company.INDUSTRY_SECTORS],
        widget=forms.Select(attrs={"class": "form-select"}),
        label=_("Industry"),
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        label=_("Show Active Only"),
    )


class AddUserToCompanyForm(forms.Form):
    """Form for adding users to a company.

    This form collects the necessary information to create a company
    membership relationship between a user and company.
    """

    user = forms.ModelChoiceField(
        queryset=User.objects.all().order_by("username"),
        widget=forms.Select(attrs={"class": "form-select"}),
        label=_("User"),
        help_text=_("Select a user to add to this company"),
    )
    role = forms.ChoiceField(
        choices=CompanyMembership.ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        label=_("Role"),
        help_text=_("Assign a role that defines the user's permissions"),
    )
    department = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-input"}),
        label=_("Department"),
        help_text=_("Department the user belongs to (optional)"),
    )
    position = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-input"}),
        label=_("Position"),
        help_text=_("User's position/title in the company (optional)"),
    )
    is_primary = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        label=_("Primary Company"),
        help_text=_("Set if this is the user's main company"),
    )
