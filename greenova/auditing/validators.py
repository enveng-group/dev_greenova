"""Custom validators for the auditing app.

This module contains reusable validators for auditing models and forms.
"""
from beartype import beartype
from django.core.exceptions import ValidationError

def validate_non_empty_description(value: str) -> None:
    """Ensure the description is not empty or whitespace only.

    Args:
        value: The string to validate.

    Raises:
        ValidationError: If the value is empty or only whitespace.
    """
    if not value or not value.strip():
        raise ValidationError("Description cannot be empty.")
