"""Forms for the Greenova landing app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from django import forms
from django.core.validators import validate_email


class NewsletterSignupForm(forms.Form):
    """Form for newsletter signup with email validation."""

    email = forms.EmailField(
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
