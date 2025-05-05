from django import forms
from django.contrib.auth import get_user_model

from .models import Company, CompanyDocument, CompanyMembership

User = get_user_model()


class CompanyForm(forms.ModelForm):
    """Form for creating and updating companies."""
    class Meta:
        model = Company
        fields = [
            'name', 'logo', 'description', 'website',
            'address', 'phone', 'email', 'company_type',
            'size', 'industry', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class CompanyMembershipForm(forms.ModelForm):
    """Form for managing company memberships."""
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = CompanyMembership
        fields = ['user', 'role', 'department', 'position', 'is_primary']


class CompanyDocumentForm(forms.ModelForm):
    """Form for uploading company documents."""
    class Meta:
        model = CompanyDocument
        fields = ['name', 'description', 'file', 'document_type']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class CompanySearchForm(forms.Form):
    """Form for searching companies."""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by name or description',
            'class': 'form-input',
            'hx-get': '/company/search/',
            'hx-trigger': 'keyup changed delay:500ms',
            'hx-target': '#company-list-container'
        })
    )
    company_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + Company.COMPANY_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'hx-get': '/company/search/',
            'hx-trigger': 'change',
            'hx-target': '#company-list-container'
        })
    )
    industry = forms.ChoiceField(
        required=False,
        choices=[('', 'All Industries')] + Company.INDUSTRY_SECTORS,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'hx-get': '/company/search/',
            'hx-trigger': 'change',
            'hx-target': '#company-list-container'
        })
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'hx-get': '/company/search/',
            'hx-trigger': 'change',
            'hx-target': '#company-list-container'
        })
    )


class AddUserToCompanyForm(forms.Form):
    """Form for adding users to a company."""
    user = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    role = forms.ChoiceField(
        choices=CompanyMembership.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    department = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    position = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    is_primary = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
