from django import forms
from .models import Obligation

class ObligationForm(forms.ModelForm):
    class Meta:
        model = Obligation
        fields = [
            # Primary Fields
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
            
            # Comments and Additional Info
            'supporting_information',
            'general_comments',
            'compliance_comments',
            'non_conformance_comments',
            'evidence',
            'person_email',
            
            # Recurrence Fields
            'recurring_obligation',
            'recurring_frequency',
            'recurring_status',
            'recurring_forcasted_date',
            
            # Inspection Fields
            'inspection',
            'inspection_frequency',
            'site_or_desktop',
            
            # Control and Analysis
            'new_control_action_required',
            'obligation_type',
            'gap_analysis',
            'notes_for_gap_analysis',
            'covered_in_which_inspection_checklist',
        ]
        widgets = {
            # Date inputs
            'action_due_date': forms.DateInput(attrs={'type': 'date'}),
            'close_out_date': forms.DateInput(attrs={'type': 'date'}),
            'recurring_forcasted_date': forms.DateInput(attrs={'type': 'date'}),
            
            # Large text fields
            'obligation': forms.Textarea(attrs={'rows': 4}),
            'supporting_information': forms.Textarea(attrs={'rows': 3}),
            'general_comments': forms.Textarea(attrs={'rows': 3}),
            'compliance_comments': forms.Textarea(attrs={'rows': 3}),
            'non_conformance_comments': forms.Textarea(attrs={'rows': 3}),
            'primary_environmental_mechanism': forms.Textarea(attrs={'rows': 3}),
            'procedure': forms.Textarea(attrs={'rows': 3}),
            'environmental_aspect': forms.Textarea(attrs={'rows': 3}),
            'gap_analysis': forms.Textarea(attrs={'rows': 3}),
            'notes_for_gap_analysis': forms.Textarea(attrs={'rows': 3}),
            
            # Checkbox fields
            'recurring_obligation': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'inspection': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'new_control_action_required': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            
            # Email field
            'person_email': forms.EmailInput(attrs={'type': 'email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        action_due_date = cleaned_data.get('action_due_date')
        close_out_date = cleaned_data.get('close_out_date')

        if close_out_date and action_due_date and close_out_date < action_due_date:
            raise forms.ValidationError("Close out date cannot be earlier than action due date")
        
        return cleaned_data

class ObligationFilterForm(forms.Form):
    STATUS_CHOICES = [('', 'All Statuses')] + list(Obligation.STATUS_CHOICES)
    PROJECT_CHOICES = [('', 'All Projects')] + list(Obligation.PROJECT_CHOICES)
    DUE_RANGE_CHOICES = [
        ('', 'All Due Dates'),
        ('overdue', 'Overdue'),
        ('7days', 'Next 7 Days'),
        ('14days', 'Next 14 Days'),
        ('month', 'Next Month'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    project = forms.ChoiceField(choices=PROJECT_CHOICES, required=False)
    due_range = forms.ChoiceField(choices=DUE_RANGE_CHOICES, required=False)
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search obligations...',
        'class': 'search-input'
    }))

class ObligationImportForm(forms.Form):
    csv_file = forms.FileField(
        label='Select CSV file',
        help_text='File must be in CSV format with required headers',
        widget=forms.FileInput(attrs={'accept': '.csv'})
    )
    
    def clean_csv_file(self):
        file = self.cleaned_data['csv_file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('File must be in CSV format')
        return file