"""Custom validators for the procedures app.

This module contains reusable validators for procedures models and forms.
"""
from beartype import beartype
from django.core.exceptions import ValidationError

def validate_document_id(value: str) -> None:
    """Validate procedure document ID format (e.g., ENV-PROC-001).

    Args:
        value: The document ID to validate.

    Raises:
        ValidationError: If the format is invalid.
    """
    if not value or not value.startswith("ENV-PROC-"):
        raise ValidationError("Document ID must start with 'ENV-PROC-'.")
