from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from typing import Any, Dict

class GreenovaUserCreationForm(UserCreationForm):
    """Enhanced user registration form."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'aria-required': 'true'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        
        # Username field
        self.fields['username'].widget.attrs.update({
            'autocomplete': 'username',
            'pattern': '[a-zA-Z0-9_]+',
            'aria-describedby': 'username-help'
        })
        
        # Password fields
        for field in ('password1', 'password2'):
            self.fields[field].widget.attrs.update({
                'autocomplete': 'new-password',
                'minlength': '8',
                'aria-required': 'true'
            })