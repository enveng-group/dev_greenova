"""Custom validators for the responsibility app.

This module contains reusable validators for responsibility models and forms.
"""
from beartype import beartype
from django.core.exceptions import ValidationError

def validate_responsibility_name(value: str) -> None:
    """Ensure responsibility name is not empty or whitespace only.

    Args:
        value: The responsibility name to validate.

    Raises:
        ValidationError: If the name is empty or only whitespace.
    """
    if not value or not value.strip():
        raise ValidationError("Responsibility name cannot be empty.")
