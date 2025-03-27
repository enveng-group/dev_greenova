import logging

from core.utils.roles import get_responsibility_choices
from django import forms
from django.core.exceptions import ValidationError
from django_select2.forms import Select2MultipleWidget
from mechanisms.models import EnvironmentalMechanism
from projects.models import Project
from responsibility.models import Responsibility

from .constants import FREQUENCY_CHOICES  # Import RESPONSIBILITY_ROLES
from .constants import STATUS_CHOICES, STATUS_COMPLETED, STATUS_NOT_STARTED
from .models import Obligation, ObligationEvidence
from .utils import normalize_frequency

logger = logging.getLogger(__name__)


class ObligationForm(forms.ModelForm):
    """Form for creating and updating obligations."""

    # Basic Information Fields
    obligation_number = forms.CharField(
        max_length=20,
        required=False,  # Auto-generated if not provided
        widget=forms.TextInput(
            attrs={
                'placeholder': 'e.g., PCEMP-001 (auto-generated if blank)',
                'aria-describedby': 'obligation_number_help',
                'class': 'form-input',
            }
        ),
    )

    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-input', 'aria-label': 'Select project'}
        ),
    )

    primary_environmental_mechanism = forms.ModelChoiceField(
        queryset=EnvironmentalMechanism.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-input',
                'aria-label': 'Select environmental mechanism',
            }
        ),
    )

    environmental_aspect = forms.ChoiceField(
        choices=[
            ('', '---------'),
            ('Air', 'Air'),
            ('Water', 'Water'),
            ('Waste', 'Waste'),
            ('Energy', 'Energy'),
            ('Biodiversity', 'Biodiversity'),
            ('Noise', 'Noise'),
            ('Chemicals', 'Chemicals'),
            ('Soil', 'Soil'),
            ('Administration', 'Administration'),
            ('Cultural Heritage Management', 'Cultural Heritage Management'),
            ('Terrestrial Fauna Management', 'Terrestrial Fauna Management'),
            ('Biosecurity And Pest Management', 'Biosecurity And Pest Management'),
            ('Dust Management', 'Dust Management'),
            ('Reporting', 'Reporting'),
            ('Noise Management', 'Noise Management'),
            (
                'Erosion And Sedimentation Management',
                'Erosion And Sedimentation Management',
            ),
            (
                'Hazardous Substances And Hydrocarbon Management',
                'Hazardous Substances And Hydrocarbon Management',
            ),
            ('Waste Management', 'Waste Management'),
            ('Artificial Light Management', 'Artificial Light Management'),
            ('Audits And Inspections', 'Audits And Inspections'),
            (
                'Design And Construction Requirements',
                'Design And Construction Requirements',
            ),
            ('Regulatory Compliance Reporting', 'Regulatory Compliance Reporting'),
            ('Other', 'Other'),
        ],
        widget=forms.Select(
            attrs={
                'class': 'form-input',
                'hx-get': '/obligations/toggle-custom-aspect/',
                'hx-target': '#custom-aspect-container',
                'hx-trigger': 'change',
                'hx-swap': 'innerHTML',
            }
        ),
    )

    custom_environmental_aspect = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Specify custom environmental aspect',
            }
        ),
    )

    obligation = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'form-input',
                'placeholder': 'Describe the environmental obligation',
            }
        )
    )

    procedure = forms.ChoiceField(
        choices=[
            ('', '---------'),
            ('Cultural Heritage Management', 'Cultural Heritage Management'),
            ('Threated Species Management', 'Threated Species Management'),
            ('Lighting Management', 'Lighting Management'),
            ('Surface Water Management', 'Surface Water Management'),
            ('Solid & Liquid Waste Management', 'Solid & Liquid Waste Management'),
            ('Dust Management', 'Dust Management'),
            ('Pest Management', 'Pest Management'),
            ('Other', 'Other'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    obligation_type = forms.ChoiceField(
        choices=[
            ('', '---------'),
            ('Training', 'Training'),
            ('Monitoring', 'Monitoring'),
            ('Reporting', 'Reporting'),
            ('Site based', 'Site based'),
            ('Incident response', 'Incident response'),
            ('Plant mobilisation', 'Plant mobilisation'),
            ('Consultations', 'Consultations'),
            ('Design', 'Design'),
            ('Procurement', 'Procurement'),
            ('Safety', 'Safety'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    # Dates and Status Fields
    action_due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-input',
                'aria-describedby': 'due_date_help',
            }
        ),
    )

    close_out_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        initial=STATUS_NOT_STARTED,
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    # Recurring Details Fields
    recurring_obligation = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
    )

    recurring_frequency = forms.ChoiceField(
        choices=FREQUENCY_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-input', 'data-conditional': 'recurring_obligation'}
        ),
    )

    recurring_status = forms.ChoiceField(
        choices=[
            ('', '---------'),
            ('not started', 'Not Started'),
            ('in progress', 'In Progress'),
            ('completed', 'Completed'),
            ('overdue', 'Overdue'),
        ],
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-input', 'data-conditional': 'recurring_obligation'}
        ),
    )

    recurring_forcasted_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-input',
                'data-conditional': 'recurring_obligation',
            }
        ),
    )

    # Inspection Details Fields
    inspection = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
    )

    inspection_frequency = forms.ChoiceField(
        choices=[
            ('', '---------'),
            ('Daily', 'Daily'),
            ('Weekly', 'Weekly'),
            ('Fortnightly', 'Fortnightly'),
            ('Monthly', 'Monthly'),
            ('Quarterly', 'Quarterly'),
            ('Annually', 'Annually'),
        ],
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-input', 'data-conditional': 'inspection'}
        ),
    )

    site_or_desktop = forms.ChoiceField(
        choices=[('', '---------'), ('Site', 'Site'), ('Desktop', 'Desktop')],
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-input', 'data-conditional': 'inspection'}
        ),
    )

    # Additional Information Fields
    accountability = forms.ChoiceField(
        choices=[
            ('', '---------'),
            ('Perdaman', 'Perdaman'),
            ('SCJV', 'SCJV'),
            ('SCJV-during construction', 'SCJV-during construction'),
            ('Perdaman-during operations', 'Perdaman-during operations'),
        ],
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    responsibility = forms.ChoiceField(
        choices=get_responsibility_choices(),
        widget=forms.Select(attrs={'class': 'form-input'}),
        label='Primary Responsibility',
        help_text='Select the primary responsibility for this obligation'
    )

    project_phase = forms.ChoiceField(
        choices=[
            ('', '---------'),
            ('Pre-Construction', 'Pre-Construction'),
            ('Construction', 'Construction'),
            ('Operation', 'Operation'),
            ('Decommissioning', 'Decommissioning'),
            ('Post-Closure', 'Post-Closure'),
            ('Other', 'Other'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    supporting_information = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'form-input',
                'placeholder': 'Any supporting information',
            }
        ),
    )

    general_comments = forms.CharField(
        required=False, widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-input'})
    )

    compliance_comments = forms.CharField(
        required=False, widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-input'})
    )

    non_conformance_comments = forms.CharField(
        required=False, widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-input'})
    )

    evidence_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'form-input',
                'placeholder': 'Notes about evidence files',
            }
        ),
    )

    new_control_action_required = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )

    gap_analysis = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )

    notes_for_gap_analysis = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'rows': 3, 'class': 'form-input', 'data-conditional': 'gap_analysis'}
        ),
    )

    covered_in_which_inspection_checklist = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-input', 'data-conditional': 'inspection'}
        ),
    )

    responsibilities = forms.ModelMultipleChoiceField(
        queryset=Responsibility.objects.all(),
        widget=Select2MultipleWidget(
            attrs={'class': 'form-input', 'aria-describedby': 'responsibilities-help'}
        ),
        required=True,  # Make this required to ensure at least one responsibility is assigned
        label='Assign Responsibilities',
        help_text='Select one or more responsibilities for this obligation',
    )

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        self.user = kwargs.pop('user', None)  # Add user context

        # Get responsibilities from kwargs if provided
        responsibilities = kwargs.pop('responsibilities', None)

        super().__init__(*args, **kwargs)

        # Initialize the responsibility queryset
        self.fields['responsibility'].choices = get_responsibility_choices()

        # Use responsibilities from the responsibility app
        if responsibilities is not None:
            self.fields['responsibilities'].queryset = responsibilities
        else:
            # Default behavior: get all responsibility roles
            self.fields['responsibilities'].queryset = Responsibility.objects.all()

        # Handle initial project
        if self.project:
            self.fields['project'].initial = self.project
            self.fields['project'].widget = forms.HiddenInput()

            # Filter mechanisms by project
            self.fields['primary_environmental_mechanism'].queryset = (
                EnvironmentalMechanism.objects.filter(project=self.project)
            )

        # Handle readonly fields for existing instance
        instance = kwargs.get('instance')
        if instance:
            self.fields['obligation_number'].widget.attrs['readonly'] = True
            self.fields['obligation_number'].help_text = (
                'Obligation ID cannot be changed'
            )
            self.fields['obligation_number'].initial = instance.obligation_number

            # Set initial values for boolean fields correctly
            for field_name in [
                'recurring_obligation',
                'inspection',
                'new_control_action_required',
                'gap_analysis',
            ]:
                if hasattr(instance, field_name):
                    self.fields[field_name].initial = getattr(instance, field_name)

            # Handle custom environmental aspect
            if instance.environmental_aspect == 'Other':
                self.fields['custom_environmental_aspect'].initial = (
                    instance.custom_environmental_aspect
                )

            self.fields['responsibilities'].initial = instance.responsibilities.all()
        else:
            self.fields['obligation_number'].help_text = (
                'Unique identifier (PCEMP-XXX format). Leave blank to auto-generate.'
            )

        # Add help text to fields
        help_texts = {
            'obligation_number': 'Unique identifier for this obligation',
            'environmental_aspect': 'Select an environmental aspect or "Other" to specify a custom aspect',
            'custom_environmental_aspect': 'Required if Environmental Aspect is "Other"',
            'action_due_date': 'When this obligation needs to be fulfilled',
            'recurring_obligation': 'Does this obligation repeat on a regular schedule?',
            'recurring_frequency': 'How often this obligation repeats',
            'inspection': 'Is an inspection required for this obligation?',
            'evidence_notes': 'Notes about uploaded evidence files',
        }

        for field, text in help_texts.items():
            if field in self.fields:
                self.fields[field].help_text = text

    def clean_obligation_number(self):
        """Validate and format obligation number if provided."""
        obligation_number = self.cleaned_data.get('obligation_number')

        # Skip validation for existing instances or if not provided
        if self.instance and self.instance.pk:
            return obligation_number

        if obligation_number:
            # Check if it matches the required format
            import re

            if not re.match(r'^PCEMP-\d+$', obligation_number):
                # Try to fix it if possible
                if obligation_number.isdigit():
                    # If it's just a number, add the prefix
                    return f'PCEMP-{obligation_number}'
                elif '-' in obligation_number:
                    # If it has a different prefix, replace it
                    parts = obligation_number.split('-', 1)
                    if len(parts) > 1 and parts[1].isdigit():
                        return f'PCEMP-{parts[1]}'

                raise ValidationError(
                    'Obligation number must be in the format PCEMP-XXX where XXX is a number.'
                )

            # Check for duplicate obligation numbers
            existing = Obligation.objects.filter(obligation_number=obligation_number)
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise ValidationError(
                    f'An obligation with number {obligation_number} already exists.'
                )

        return obligation_number

    def clean_recurring_frequency(self):
        """Normalize recurring frequency if provided."""
        frequency = self.cleaned_data.get('recurring_frequency')
        recurring = self.cleaned_data.get('recurring_obligation')

        if recurring and not frequency:
            raise ValidationError('Frequency is required for recurring obligations')

        if not recurring:
            return ''

        # Normalize the frequency
        return normalize_frequency(frequency)

    def clean_custom_environmental_aspect(self):
        """Validate custom aspect is provided when needed."""
        aspect = self.cleaned_data.get('environmental_aspect')
        custom_aspect = self.cleaned_data.get('custom_environmental_aspect')

        if aspect == 'Other' and not custom_aspect:
            raise ValidationError('Please specify a custom environmental aspect.')

        return custom_aspect

    def clean_responsibilities(self):
        """Validate at least one responsibility is selected."""
        responsibilities = self.cleaned_data.get('responsibilities')
        if not responsibilities or len(responsibilities) == 0:
            raise forms.ValidationError('Please select at least one responsibility.')
        return responsibilities

    def clean(self):
        """Cross-field validation to enforce business rules."""
        cleaned_data = super().clean()

        # Check date relationships - close_out_date should be after action_due_date
        action_due_date = cleaned_data.get('action_due_date')
        close_out_date = cleaned_data.get('close_out_date')
        status = cleaned_data.get('status')

        if close_out_date and action_due_date and close_out_date < action_due_date:
            self.add_error(
                'close_out_date', 'Close out date must be after action due date'
            )

        # If status is completed, require close_out_date
        if status == STATUS_COMPLETED and not close_out_date:
            self.add_error(
                'close_out_date', 'Close out date is required when status is completed'
            )

        # Validate recurring fields
        recurring = cleaned_data.get('recurring_obligation')
        if recurring:
            for field in ['recurring_frequency', 'recurring_status']:
                if not cleaned_data.get(field):
                    self.add_error(
                        field,
                        f'{field.replace("_", " ").title()} is required for recurring obligations',
                    )

        # Validate inspection fields
        inspection = cleaned_data.get('inspection')
        if inspection:
            for field in ['inspection_frequency', 'site_or_desktop']:
                if not cleaned_data.get(field):
                    self.add_error(
                        field,
                        f'{field.replace("_", " ").title()} is required when inspection is enabled',
                    )

        # Validate gap analysis notes
        gap_analysis = cleaned_data.get('gap_analysis')
        if gap_analysis and not cleaned_data.get('notes_for_gap_analysis'):
            self.add_error(
                'notes_for_gap_analysis',
                'Notes are required when gap analysis is enabled',
            )

        return cleaned_data

    def save(self, commit=True):
        """Override save to ensure obligation_number is set for new instances."""
        instance = super().save(commit=False)

        # For new instances without a number, generate one
        if not instance.pk and not instance.obligation_number:
            instance.obligation_number = Obligation.get_next_obligation_number()

        # Copy custom environmental aspect if needed
        if instance.environmental_aspect == 'Other':
            instance.custom_environmental_aspect = self.cleaned_data.get(
                'custom_environmental_aspect', ''
            )

        # Handle recurring forecasted date
        if instance.recurring_obligation and not instance.recurring_forcasted_date:
            instance.update_recurring_forecasted_date()

        if commit:
            instance.save()
            self.save_m2m()  # Save Many-to-Many relationships

        return instance

    class Meta:
        model = Obligation
        fields = '__all__'
        exclude = [
            'person_email'
        ]  # This field appears to be unused based on the templates
        widgets = {
            'obligation': forms.Textarea(attrs={'rows': 4}),
            'supporting_information': forms.Textarea(attrs={'rows': 3}),
            'general_comments': forms.Textarea(attrs={'rows': 3}),
            'compliance_comments': forms.Textarea(attrs={'rows': 3}),
            'non_conformance_comments': forms.Textarea(attrs={'rows': 3}),
            'evidence_notes': forms.Textarea(attrs={'rows': 2}),
            'notes_for_gap_analysis': forms.Textarea(attrs={'rows': 3}),
            'action_due_date': forms.DateInput(attrs={'type': 'date'}),
            'close_out_date': forms.DateInput(attrs={'type': 'date'}),
            'recurring_forcasted_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'primary_environmental_mechanism': 'Environmental Mechanism',
            'action_due_date': 'Due Date',
            'recurring_forcasted_date': 'Next Forecasted Due Date',
        }
        help_texts = {
            'environmental_aspect': 'Select the environmental aspect this obligation relates to',
            'custom_environmental_aspect': 'If "Other" is selected above, please specify the aspect',
            'obligation': 'Describe the specific obligation requirement',
            'recurring_obligation': 'Does this obligation recur on a regular schedule?',
            'inspection': 'Does this obligation require inspections?',
            'gap_analysis': 'Is a gap analysis required for this obligation?',
        }


class EvidenceUploadForm(forms.ModelForm):
    """Form for uploading evidence files."""

    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-input',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.png,.jpg,.jpeg,.gif,.txt,.csv',
            }
        ),
        help_text='Upload evidence files (max 25MB). Allowed formats: PDF, DOC, DOCX, XLS, XLSX, PNG, JPG, JPEG, GIF, TXT, CSV',
    )

    description = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Brief description of the evidence file',
            }
        ),
    )

    def clean_file(self):
        """Validate file size and extension."""
        file = self.cleaned_data.get('file')
        if file:
            # Validate file size (25MB limit)
            if file.size > 26214400:  # 25MB in bytes
                raise ValidationError('File size must be under 25MB')

            # Validate file extension
            allowed_extensions = [
                'pdf',
                'doc',
                'docx',
                'xls',
                'xlsx',
                'png',
                'jpg',
                'jpeg',
                'gif',
                'txt',
                'csv',
            ]

            file_ext = file.name.split('.')[-1].lower()
            if file_ext not in allowed_extensions:
                raise ValidationError(
                    f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
                )

            # Check if this obligation already has 5 files
            if self.instance and self.instance.obligation:
                if (
                    ObligationEvidence.objects.filter(
                        obligation=self.instance.obligation
                    ).count()
                    >= 5
                ):
                    raise ValidationError(
                        'Maximum of 5 evidence files allowed per obligation'
                    )

        return file

    class Meta:
        model = ObligationEvidence
        fields = ['file', 'description']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Brief description of the file'}),
        }
