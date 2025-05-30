"""Copyright (C) 2025 Adrian Gallo.

This file is part of Greenova.

Greenova is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Greenova is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Greenova. If not, see <https://www.gnu.org/licenses/>.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

"""Forms for the obligations app.

Defines forms for creating, updating, and validating environmental obligations
and evidence uploads.
"""


from models import Obligation, ObligationEvidence
from typing import ClassVar
from django import forms


class ObligationForm(forms.ModelForm):
    """Form for creating and updating obligations."""

    def __init__(self, *args: object, **kwargs: object) -> None:
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
