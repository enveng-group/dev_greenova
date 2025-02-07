from django import forms
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from .models import Obligation


class ObligationForm(forms.ModelForm):
    """Form for creating and editing obligations."""

    class Meta:
        model = Obligation
        fields = [
            'obligation_number',
            'project_name',
            'primary_environmental_mechanism',
            'procedure',
            'environmental_aspect',
            'obligation',
            'accountability',
            'responsibility',
            'project_phase',
            'action_due_date',
            'close_out_date',
            'status',
            'supporting_information',
            'general_comments',
            'compliance_comments',
            'non_conformance_comments',
            'evidence',
            'person_email',
            'recurring_obligation',
            'recurring_frequency',
            'recurring_status',
            'recurring_forcasted_date',
            'inspection',
            'inspection_frequency',
            'site_or_desktop',
            'new_control_action_required',
            'obligation_type',
            'gap_analysis',
            'notes_for_gap_analysis',
            'covered_in_which_inspection_checklist',
        ]
        widgets = {
            'action_due_date': forms.DateInput(attrs={'type': 'date'}),
            'close_out_date': forms.DateInput(attrs={'type': 'date'}),
            'recurring_forcasted_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'supporting_information': forms.Textarea(attrs={'rows': 3}),
            'general_comments': forms.Textarea(attrs={'rows': 3}),
            'compliance_comments': forms.Textarea(attrs={'rows': 3}),
            'non_conformance_comments': forms.Textarea(attrs={'rows': 3}),
            'gap_analysis': forms.Textarea(attrs={'rows': 3}),
            'notes_for_gap_analysis': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_person_email(self):
        """Validate email format."""
        email = self.cleaned_data.get('person_email')
        if email:
            # Basic email validation
            if '@' not in email:
                raise forms.ValidationError(_('Enter a valid email address'))
        return email


class ObligationFilterForm(forms.Form):
    """Form for filtering obligations in list view."""

    project_name = forms.CharField(required=False)
    status = forms.ChoiceField(
        choices=[('', 'All')] + Obligation.STATUS_CHOICES, required=False
    )
    responsibility = forms.CharField(required=False)
    due_date_from = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
    due_date_to = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
    recurring_only = forms.BooleanField(required=False)
    inspection_only = forms.BooleanField(required=False)

    def clean(self):
        """Validate date range if both dates are provided."""
        cleaned_data = super().clean()
        date_from = cleaned_data.get('due_date_from')
        date_to = cleaned_data.get('due_date_to')

        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError(
                _('Start date must be before end date')
            )
        return cleaned_data


class ObligationSearchForm(forms.Form):
    """Form for searching obligations."""

    q = forms.CharField(
        label=_('Search'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Search obligations...'),
                'class': 'search-input',
            }
        ),
    )


class ObligationImportForm(forms.Form):
    """Form for importing obligations from CSV."""

    file = forms.FileField(
        label=_('CSV File'),
        validators=[FileExtensionValidator(allowed_extensions=['csv'])],
    )
    update_existing = forms.BooleanField(
        required=False,
        initial=False,
        help_text=_('Update existing obligations if they exist'),
    )
