"""Custom validators for the authentication app.

This module contains reusable validators for authentication models and forms.
"""
from beartype import beartype
from django.core.exceptions import ValidationError
import re

def validate_username(value: str) -> None:
    """Ensure the username meets project requirements.

    Args:
        value: The username to validate.

    Raises:
        ValidationError: If the username is invalid.
    """
    if not re.match(r"^[\w.@+-]+$", value):
        raise ValidationError("Username contains invalid characters.")
    if len(value) < 3:
        raise ValidationError("Username must be at least 3 characters long.")

def validate_email_unique(value: str) -> None:
    """Ensure the email is unique (example placeholder).

    Args:
        value: The email to validate.

    Raises:
        ValidationError: If the email is not unique.
    """
    # Implement uniqueness check in form/model clean method as needed.
    pass
