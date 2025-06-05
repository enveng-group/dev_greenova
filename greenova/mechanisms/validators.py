"""Custom validators for the mechanisms app.

This module contains reusable validators for mechanisms models and forms.
"""
from beartype import beartype
from django.core.exceptions import ValidationError

def validate_reference_number(value: str) -> None:
    """Validate the reference number format for mechanisms.

    Args:
        value: The reference number to validate.

    Raises:
        ValidationError: If the reference number is invalid.
    """
    if not value or not value.strip():
        raise ValidationError("Reference number cannot be empty.")
