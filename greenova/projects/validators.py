"""Custom validators for the projects app.

This module contains reusable validators for projects models and forms.
"""
from beartype import beartype
from django.core.exceptions import ValidationError

def validate_project_name(value: str) -> None:
    """Ensure project name is not empty or whitespace only.

    Args:
        value: The project name to validate.

    Raises:
        ValidationError: If the name is empty or only whitespace.
    """
    if not value or not value.strip():
        raise ValidationError("Project name cannot be empty.")
