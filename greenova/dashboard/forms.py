"""Copyright (C) 2024 Adrian Gallo <agallo@enveng-group.com.au>
This file is part of Greenova and is licensed under the AGPL-3.0.

Dashboard app forms for Greenova.

Forms for project and mechanism creation.
"""

from typing import Any

from beartype import beartype
from crispy_forms.helper import FormHelper  # type: ignore[import]
from crispy_forms.layout import Submit  # type: ignore[import]
from django import forms
from django_bootstrap5.widgets import RadioSelectButtonGroup  # type: ignore[import]


@beartype
class DashboardStubForm(forms.Form):
    """Stub form for dashboard app, using Bootstrap 5 and crispy-forms.

    This is a placeholder for future dashboard forms. Uses Bootstrap 5 markup
    and crispy-forms for rendering.
    """

    name = forms.CharField(
        max_length=128,
        label="Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter name"},
        ),
    )
    type = forms.ChoiceField(
        choices=[("summary", "Summary"), ("chart", "Chart")],
        label="Type",
        widget=RadioSelectButtonGroup,
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize DashboardStubForm with crispy-forms helper and Bootstrap 5.

        Args:
            *args: Positional arguments for the parent Form.
            **kwargs: Keyword arguments for the parent Form.

        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit", css_class="btn btn-primary"))
