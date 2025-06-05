"""Custom validators for the obligations app.

This module contains reusable validators for obligations models and forms.
"""
from beartype import beartype
from django.core.exceptions import ValidationError
import re

def validate_obligation_number(value: str) -> None:
    """Validate obligation number format (e.g., PCEMP-001).

    Args:
        value: The obligation number to validate.

    Raises:
        ValidationError: If the format is invalid.
    """
    if not re.match(r"^PCEMP-\d{3}$", value):
        raise ValidationError("Obligation number must be in format PCEMP-XXX.")

def validate_non_empty_field(value: str) -> None:
    """Ensure a field is not empty or whitespace only.

    Args:
        value: The string to validate.

    Raises:
        ValidationError: If the value is empty or only whitespace.
    """
    if not value or not value.strip():
        raise ValidationError("This field cannot be empty.")
