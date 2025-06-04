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
        super().__init__(*args, **kwargs)


class CorrectiveActionForm(forms.ModelForm):
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
        super().__init__(*args, **kwargs)


class AuditEntryForm(forms.ModelForm):
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
        super().__init__(*args, **kwargs)


class ComplianceCommentForm(forms.ModelForm):
    obligation = forms.ModelChoiceField(
        queryset=Obligation.objects.all(),
        widget=autocomplete.ModelSelect2(url="obligation-autocomplete"),
    )

    class Meta:
        model = ComplianceComment
        fields = ["obligation", "text"]

    @beartype
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


class NonConformanceCommentForm(forms.ModelForm):
    obligation = forms.ModelChoiceField(
        queryset=Obligation.objects.all(),
        widget=autocomplete.ModelSelect2(url="obligation-autocomplete"),
    )

    class Meta:
        model = NonConformanceComment
        fields = ["obligation", "text"]

    @beartype
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


# NOTE: You must implement the corresponding autocomplete views and urls for each ModelSelect2 widget above.
# See the django-autocomplete-light documentation for details.
