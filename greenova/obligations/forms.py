import logging
from django import forms
from django.utils import timezone
from .models import Obligation
from mechanisms.models import EnvironmentalMechanism
from projects.models import Project
from django.core.exceptions import ValidationError
from .models import ObligationEvidence
from .constants import STATUS_CHOICES, STATUS_COMPLETED, FREQUENCY_CHOICES

logger = logging.getLogger(__name__)

class ObligationForm(forms.ModelForm):
    """Form for creating and updating obligations."""

    # Enhanced fields with better widgets and validation
    obligation_number = forms.CharField(
        max_length=20,
        required=False,  # Make it optional in the form
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., PCEMP-001 (leave blank for auto-generation)',
            'aria-describedby': 'obligation_number_help',
            'class': 'form-input'
        })
    )

    environmental_aspect = forms.ChoiceField(
        choices=[
            ('Air', 'Air'),
            ('Water', 'Water'),
            ('Waste', 'Waste'),
            ('Energy', 'Energy'),
            ('Biodiversity', 'Biodiversity'),
            ('Noise', 'Noise'),
            ('Chemicals', 'Chemicals'),
            ('Soil', 'Soil'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            'class': 'form-input',
            'hx-get': '/obligations/toggle-custom-aspect/',
            'hx-target': '#custom-aspect-container',
            'hx-trigger': 'change',
            'hx-swap': 'innerHTML'
        })
    )

    custom_environmental_aspect = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'style': 'display:none;'
        })
    )

    obligation = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Describe the environmental obligation',
            'rows': 3,
            'class': 'form-input'
        })
    )

    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    primary_environmental_mechanism = forms.ModelChoiceField(
        queryset=EnvironmentalMechanism.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    accountability = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    responsibility = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    project_phase = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    procedure = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'form-input'
        })
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    action_due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'aria-describedby': 'due_date_help',
            'class': 'form-input'
        })
    )

    close_out_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-input'
        })
    )

    supporting_information = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'form-input',
            'placeholder': 'Any supporting information'
        })
    )

    general_comments = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'form-input'
        })
    )

    compliance_comments = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'form-input'
        })
    )

    non_conformance_comments = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'form-input'
        })
    )

    evidence = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'form-input',
            'placeholder': 'Describe the evidence provided'
        })
    )

    recurring_obligation = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )

    recurring_frequency = forms.ChoiceField(
        choices=FREQUENCY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-input',
            'id': 'id_recurring_frequency',
            'aria-describedby': 'recurring_frequency_help'
        })
    )

    recurring_status = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    recurring_forcasted_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-input'
        })
    )

    inspection = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )

    inspection_frequency = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    site_or_desktop = forms.ChoiceField(
        choices=[('Site', 'Site'), ('Desktop', 'Desktop')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    new_control_action_required = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )

    obligation_type = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    gap_analysis = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'form-input'
        })
    )

    notes_for_gap_analysis = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'form-input'
        })
    )

    # Additional help text for fields
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

        # Set initial project if provided
        if self.project:
            self.fields['project'].initial = self.project
            self.fields['project'].widget = forms.HiddenInput()

        # If editing an existing obligation, make obligation_number readonly
        instance = kwargs.get('instance')
        if instance:
            self.fields['obligation_number'].widget.attrs['readonly'] = True
            self.fields['obligation_number'].help_text = 'Obligation ID cannot be changed'
        else:
            self.fields['obligation_number'].help_text = 'Unique identifier (PCEMP-XXX format). Leave blank to auto-generate.'

        # Update mechanism choices based on project
        if self.project:
            self.fields['primary_environmental_mechanism'].queryset = (
                EnvironmentalMechanism.objects.filter(project=self.project)
            )

        # Add help text
        self.fields['obligation_number'].help_text = 'Unique identifier for this obligation'
        self.fields['action_due_date'].help_text = 'When this obligation needs to be fulfilled'
        self.fields['recurring_obligation'].help_text = 'Does this obligation repeat regularly?'
        self.fields['inspection'].help_text = 'Is an inspection required for this obligation?'
        self.fields['new_control_action_required'].help_text = 'Is a new control action required?'

        # Improve field organization with fieldsets via widget attributes
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.HiddenInput, forms.CheckboxInput)):
                field.widget.attrs.update({'class': 'form-input'})

        # If 'Other' is already selected, show the custom field
        if self.initial.get('environmental_aspect') == 'Other':
            self.fields['custom_environmental_aspect'].widget.attrs['style'] = 'display:block;'
        else:
            self.fields['custom_environmental_aspect'].widget.attrs['style'] = 'display:none;'

    def clean_obligation_number(self):
        """Ensure obligation_number format is valid if provided."""
        obligation_number = self.cleaned_data.get('obligation_number')

        if obligation_number:
            # Check if it matches the required format
            import re
            if not re.match(r'^PCEMP-\d+$', obligation_number):
                # Try to fix it if possible
                if obligation_number.isdigit():
                    # If it's just a number, add the prefix
                    return f"PCEMP-{obligation_number}"
                elif '-' in obligation_number:
                    # If it has a different prefix, replace it
                    parts = obligation_number.split('-', 1)
                    if len(parts) > 1 and parts[1].isdigit():
                        return f"PCEMP-{parts[1]}"

                raise forms.ValidationError(
                    "Obligation number must be in the format PCEMP-XXX where XXX is a number."
                )

        return obligation_number

    def clean_recurring_frequency(self):
        """Ensure recurring frequency is normalized."""
        frequency = self.cleaned_data.get('recurring_frequency')
        recurring = self.cleaned_data.get('recurring_obligation')

        if recurring and not frequency:
            raise forms.ValidationError("Frequency is required for recurring obligations")

        if not recurring:
            return ''

        # Normalize the frequency
        from .utils import normalize_frequency
        return normalize_frequency(frequency)

    def clean(self):
        """Custom validation to enforce business rules."""
        cleaned_data = super().clean()

        # Check date relationships - close_out_date should be after action_due_date
        action_due_date = cleaned_data.get('action_due_date')
        close_out_date = cleaned_data.get('close_out_date')
        status = cleaned_data.get('status')

        if close_out_date and action_due_date and close_out_date < action_due_date:
            self.add_error('close_out_date', 'Close out date must be after action due date')

        # If status is completed, require close_out_date
        if status == STATUS_COMPLETED and not close_out_date:
            self.add_error('close_out_date', 'Close out date is required when status is completed')

        # If recurring is checked, require frequency
        recurring = cleaned_data.get('recurring_obligation')
        recurring_frequency = cleaned_data.get('recurring_frequency')
        if recurring and not recurring_frequency:
            self.add_error('recurring_frequency', 'Frequency is required for recurring obligations')

        # Validate custom aspect is provided if 'Other' is selected
        environmental_aspect = cleaned_data.get('environmental_aspect')
        custom_aspect = cleaned_data.get('custom_environmental_aspect')
        if environmental_aspect == 'Other' and not custom_aspect:
            self.add_error('custom_environmental_aspect',
                          'Please specify the custom environmental aspect.')

        return cleaned_data

    class Meta:
        model = Obligation
        fields = '__all__'

class EvidenceUploadForm(forms.ModelForm):
    class Meta:
        model = ObligationEvidence
        fields = ['file', 'description']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 26214400:  # 25MB limit
                raise ValidationError("File size must be under 25MB")

            # Check if this obligation already has 5 files
            if self.instance and self.instance.obligation:
                if ObligationEvidence.objects.filter(obligation=self.instance.obligation).count() >= 5:
                    raise ValidationError("Maximum of 5 evidence files allowed per obligation")
        return file
