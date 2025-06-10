from typing import Any

from django import forms

class DashboardStubForm(forms.Form):
    name: forms.CharField

class AddObligationForm(forms.Form):
    title: forms.CharField
    description: forms.CharField
    status: forms.ChoiceField
    due_date: forms.DateField
    helper: Any
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
