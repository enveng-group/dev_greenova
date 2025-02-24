from django import forms
from typing import Dict
import logging
from .models import Obligation

logger = logging.getLogger(__name__)


class ObligationForm(forms.ModelForm):
    class Meta:
        model = Obligation
        fields = [
            'obligation_number',
            'mechanism',
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
