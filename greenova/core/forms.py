"""Forms for the Greenova core app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from django import forms

from .models import EnvironmentalObligation

# Example for autocomplete integration:
# from .models import Project
# from dal import autocomplete


class EnvironmentalObligationForm(forms.ModelForm):
    """Form for EnvironmentalObligation with autocomplete for large select fields."""

    # Example usage for a large ForeignKey field:
    # project = forms.ModelChoiceField(
    #     queryset=Project.objects.all(),
    #     widget=autocomplete.ModelSelect2(url="project-autocomplete"),
    # )

    class Meta:
        model = EnvironmentalObligation
        fields = [
            "name",
            "description",
            "due_date",
            "is_complete",
            # "project",  # Uncomment if ForeignKey exists
        ]
        widgets = {
            # 'project': autocomplete.ModelSelect2(url='project-autocomplete'),
        }
