from django import forms
from typing import Any, Dict
import logging
from .models import Project, Obligation

logger = logging.getLogger(__name__)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        
    def clean(self) -> Dict[str, Any]:
        try:
            cleaned_data = super().clean()
            logger.debug(f"Validating project form data: {cleaned_data}")
            name = cleaned_data.get('name')
            if name and Project.objects.filter(name=name).exists():
                self.add_error('name', 'A project with this name already exists.')
            return cleaned_data
        except Exception as e:
            logger.error(f"Form validation error: {str(e)}")
            raise

class ObligationForm(forms.ModelForm):
    class Meta:
        model = Obligation
        fields = [
            'obligation_number',
            'primary_environmental_mechanism',
            'environmental_aspect',
            'obligation',
            'accountability',
            'responsibility',
            'status',
            'action_due_date'
        ]
        widgets: Dict[str, forms.Widget] = {
            'action_due_date': forms.DateInput(attrs={'type': 'date'}),
            'obligation': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_obligation_number(self) -> str:
        number = self.cleaned_data['obligation_number']
        if (Obligation.objects.filter(obligation_number=number)
                            .exclude(pk=self.instance.pk if self.instance else None)
                            .exists()):
            raise forms.ValidationError('This obligation number already exists.')
        return number