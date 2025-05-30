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

"""Forms for the chatbot app.

This module defines forms for creating conversations and training data in the
chatbot application.
"""


from django import forms
from .models import Conversation, TrainingData
from typing import ClassVar


class ConversationForm(forms.ModelForm):
    """Form for creating a new conversation."""

    class Meta:
        """Meta options for ConversationForm.

        Specifies the model and fields for the form.
        """

        model = Conversation
        fields: ClassVar[list[str]] = ["title"]
        widgets: ClassVar[dict[str, forms.Widget]] = {
            "title": forms.TextInput(
                attrs={"class": "input", "placeholder": "Conversation Title"},
            ),
        }


class TrainingDataForm(forms.ModelForm):
    """Form for adding new training data."""

    class Meta:
        """Meta options for TrainingDataForm.

        Specifies the model and fields for the form.
        """

        model = TrainingData
        fields: ClassVar[list[str]] = ["question", "answer", "category"]
        widgets: ClassVar[dict[str, forms.Widget]] = {
            "question": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Enter question"},
            ),
            "answer": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Enter answer"},
            ),
            "category": forms.TextInput(
                attrs={"placeholder": "Category (optional)"},
            ),
        }
