"""Forms for the Greenova landing app.

NewsletterSignupForm provides email validation and sanitization for the newsletter signup form.
Form data is serialized/deserialized using Protobuf3 in the view layer.
See landing/serializers.py for API serialization details.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from typing import Any

import bleach
from django import forms
from django.core.validators import validate_email


class NewsletterSignupForm(forms.Form):
    """Form for newsletter signup with email validation.

    Fields:
        email: Email address for newsletter signup.
    """

    email: forms.EmailField

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the newsletter signup form."""
        super().__init__(*args, **kwargs)
        self.fields["email"] = forms.EmailField(
            label="Email address",
            max_length=254,
            widget=forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your email for updates",
                    "aria-label": "Email address for newsletter",
                    "required": True,
                    "id": "id_email",
                },
            ),
            validators=[validate_email],
        )

    def clean_email(self) -> str:
        """Sanitize and validate the email field using bleach."""
        email = self.cleaned_data.get("email", "")
        sanitized_email = bleach.clean(email, strip=True)
        self.cleaned_data["email"] = sanitized_email
        return sanitized_email
