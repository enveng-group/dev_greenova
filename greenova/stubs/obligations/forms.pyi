from .models import Obligation, ObligationEvidence
from _typeshed import Incomplete
from django import forms

logger: Incomplete

class ObligationForm(forms.ModelForm):
    obligation_number: Incomplete
    project: forms.ModelChoiceField
    primary_environmental_mechanism: forms.ModelChoiceField
    environmental_aspect: forms.ChoiceField
    custom_environmental_aspect: forms.CharField
    obligation: forms.CharField
    procedure: forms.ChoiceField
    obligation_type: forms.ChoiceField
    action_due_date: forms.DateField
    close_out_date: forms.DateField
    status: forms.ChoiceField
    recurring_obligation: forms.BooleanField
    recurring_frequency: forms.ChoiceField
    recurring_status: forms.ChoiceField
    recurring_forecasted_date: forms.DateField
    inspection: forms.BooleanField
    inspection_frequency: forms.ChoiceField
    site_or_desktop: forms.ChoiceField
    accountability: forms.ChoiceField
    responsibility: forms.ChoiceField
    project_phase: forms.ChoiceField
    supporting_information: forms.CharField
    general_comments: forms.CharField
    compliance_comments: forms.CharField
    non_conformance_comments: forms.CharField
    evidence_notes: forms.CharField
    new_control_action_required: forms.BooleanField
    gap_analysis: forms.BooleanField
    notes_for_gap_analysis: forms.CharField
    covered_in_which_inspection_checklist: forms.CharField
    responsibilities: forms.ModelMultipleChoiceField
    user: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def clean_obligation_number(self): ...
    def clean_recurring_frequency(self): ...
    def clean_custom_environmental_aspect(self): ...
    def clean_responsibilities(self): ...
    def clean(self): ...
    def save(self, commit: bool = True): ...
    class Meta:
        model = Obligation
        fields: str
        widgets: Incomplete
        labels: Incomplete
        help_texts: Incomplete

class EvidenceUploadForm(forms.ModelForm):
    file: Incomplete
    description: Incomplete
    def clean_file(self): ...
    class Meta:
        model = ObligationEvidence
        fields: Incomplete
        widgets: Incomplete
