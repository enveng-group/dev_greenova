"""Custom validators for the users app.

This module contains reusable validators for users models and forms.
"""
from beartype import beartype
from django.core.exceptions import ValidationError
import re

def validate_phone_number(value: str) -> None:
    """Validate phone number format (basic example).

    Args:
        value: The phone number to validate.

    Raises:
        ValidationError: If the phone number is invalid.
    """
    if value and not re.match(r"^\+?\d{7,15}$", value):
        raise ValidationError("Enter a valid phone number.")
