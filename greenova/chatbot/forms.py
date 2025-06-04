from beartype import beartype
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit
from django import forms

from .models import Conversation, TrainingData


class ConversationForm(forms.ModelForm):
    """Form for creating a new conversation.

    Attributes:
        helper (FormHelper): Helper for crispy forms layout.

    """

    @beartype
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Conversation Details",
                "title",
            ),
            Submit("submit", "Create Conversation"),
        )

    class Meta:
        model = Conversation
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "input", "placeholder": "Conversation Title"},
            ),
        }
        # Example: widgets = {"intent": forms.Select(choices=INTENT_CHOICES)}


class TrainingDataForm(forms.ModelForm):
    """Form for adding new training data.

    Attributes:
        helper (FormHelper): Helper for crispy forms layout.

    """

    @beartype
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Training Data",
                "question",
                "answer",
                "category",
            ),
            Submit("submit", "Add Training Data"),
        )

    class Meta:
        model = TrainingData
        fields = ["question", "answer", "category"]
        widgets = {
            "question": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Enter question"},
            ),
            "answer": forms.Textarea(attrs={"rows": 5, "placeholder": "Enter answer"}),
            "category": forms.TextInput(attrs={"placeholder": "Category (optional)"}),
        }
        # Example: widgets = {"message_type": forms.Select(choices=MESSAGE_TYPE_CHOICES)}
