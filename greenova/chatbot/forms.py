from django import forms

from .models import Conversation, TrainingData


class ConversationForm(forms.ModelForm):
    """Form for creating a new conversation."""
    class Meta:
        model = Conversation
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Conversation Title'})
        }

class TrainingDataForm(forms.ModelForm):
    """Form for adding new training data."""
    class Meta:
        model = TrainingData
        fields = ['question', 'answer', 'category']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter question'}),
            'answer': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter answer'}),
            'category': forms.TextInput(attrs={'placeholder': 'Category (optional)'})
        }
