"""Forms for the obligations app.

Defines forms for creating, updating, and validating environmental obligations
and evidence uploads.
"""
from typing import ClassVar

from django import forms
from models import Obligation, ObligationEvidence


class ObligationForm(forms.ModelForm):
    """Form for creating and updating obligations."""

    def __init__(self, *args, **kwargs):
        """Initialize ObligationForm with project, user, and responsibilities."""
        self.project = kwargs.pop("project", None)
        self.user = kwargs.pop("user", None)  # Add user context
        super().__init__(*args, **kwargs)

    class Meta:
        """Meta options for ObligationForm."""

        model = Obligation
        fields = "__all__"


class EvidenceUploadForm(forms.ModelForm):
    """Form for uploading evidence files."""

    class Meta:
        """Meta options for EvidenceUploadForm."""

        model: type[ObligationEvidence] = ObligationEvidence
        fields: ClassVar[list[str]] = ["file", "description"]
