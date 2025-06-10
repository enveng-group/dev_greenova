"""Forms for the Greenova landing app.

NewsletterSignupForm provides email validation and sanitization for the newsletter signup form.
Form data is serialized/deserialized using Protobuf3 in the view layer.
See landing/serializers.py for API serialization details.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from beartype import beartype
from django import forms
from django.core.validators import validate_email


class NewsletterSignupForm(forms.Form):
    """Form for newsletter signup with email validation and sanitization.

    Fields:
        email: Email address for newsletter signup.
    """

    email = forms.EmailField(
        label="Email address",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
                "autocomplete": "email",
                "required": True,
            }
        ),
        validators=[validate_email],
    )

    @beartype
    def clean_email(self) -> str:
        """Sanitize and validate the email address."""
        email = self.cleaned_data["email"].strip().lower()
        validate_email(email)
        return email
