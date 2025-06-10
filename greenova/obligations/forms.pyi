from typing import Any

from _typeshed import Incomplete
from beartype import beartype
from django import forms

from .models import Obligation as Obligation
from .models import ObligationEvidence as ObligationEvidence

User: Incomplete
logger: Incomplete
ResponsibilityAssignmentFormSet: Incomplete

class FilterForm(forms.Form):
    @beartype
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    @beartype
    def clean(self) -> dict[str, Any]: ...

class ObligationForm(forms.ModelForm):
    project: Incomplete
    user: Incomplete
    @beartype
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    @beartype
    def clean_obligation_number(self) -> str | None: ...
    @beartype
    def clean_recurring_frequency(self) -> str: ...
    @beartype
    def clean_custom_environmental_aspect(self) -> str: ...
    @beartype
    def clean_obligation(self) -> str: ...
    @beartype
    def clean_supporting_information(self) -> str: ...
    @beartype
    def clean(self) -> dict[str, Any]: ...
    @beartype
    def save(self, commit: bool = True) -> Obligation: ...
    class Meta:
        model = Obligation
        fields: str
        exclude: Incomplete
        widgets: dict[str, forms.Widget]
        labels: Incomplete
        help_texts: Incomplete

class ResponsibilityAssignmentForm(forms.Form):
    user: Incomplete
    responsibility: Incomplete

class ObligationResponsibilityForm(forms.Form):
    assignments: Incomplete

class EvidenceUploadForm(forms.ModelForm):
    file: Incomplete
    description: Incomplete
    @beartype
    def clean_file(self) -> Any: ...
    class Meta:
        model = ObligationEvidence
        fields: Incomplete
        widgets: Incomplete

class ObligationFilterForm(forms.Form):
    search: Incomplete
    status: Incomplete
    phase: Incomplete
    sort: Incomplete
