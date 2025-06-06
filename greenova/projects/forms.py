# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Forms for the projects app.

This module provides forms for creating and updating Project instances, using
crispy-forms for rendering and bleach for sanitizing user input.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

import bleach
from beartype import beartype
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    """Form for creating and updating Project instances."""

    @beartype
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save Project"))

    @beartype
    def clean_description(self) -> str:
        description = self.cleaned_data.get("description", "")
        return bleach.clean(description)

    class Meta:
        model = Project
        fields = ["name", "description"]
