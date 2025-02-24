from django import forms


class ChatMessageForm(forms.Form):
    """Form for handling chat messages."""
    message = forms.CharField(
        max_length=1000,
        required=True,
        error_messages={
            'required': 'Message cannot be empty',
            'max_length': 'Message too long (max 1000 characters)'
        }
    )

    def clean_message(self):
        """Clean and validate message content."""
        message = self.cleaned_data['message'].strip()
        if not message:
            raise forms.ValidationError('Message cannot be empty')
        return message
