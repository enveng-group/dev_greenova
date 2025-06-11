from .models import Company, CompanyDocument, CompanyMembership
from _typeshed import Incomplete
from django import forms

logger: Incomplete
User: Incomplete

class CompanyForm(forms.ModelForm):
    def clean(self): ...
    class Meta:
        model = Company
        fields: Incomplete
        widgets: Incomplete
        labels: Incomplete
        help_texts: Incomplete

class CompanyMembershipForm(forms.ModelForm):
    user: Incomplete
    class Meta:
        model = CompanyMembership
        fields: Incomplete
        labels: Incomplete
        help_texts: Incomplete

class CompanyDocumentForm(forms.ModelForm):
    class Meta:
        model = CompanyDocument
        fields: Incomplete
        widgets: Incomplete
        labels: Incomplete
        help_texts: Incomplete

class CompanySearchForm(forms.Form):
    search: Incomplete
    company_type: Incomplete
    industry: Incomplete
    is_active: Incomplete

class AddUserToCompanyForm(forms.Form):
    user: Incomplete
    role: Incomplete
    department: Incomplete
    position: Incomplete
    is_primary: Incomplete
