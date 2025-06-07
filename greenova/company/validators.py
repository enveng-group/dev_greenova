"""Custom validators for the company app.

This module contains reusable validators for company models and forms.
"""

import re

from django.core.exceptions import ValidationError


def validate_abn(value: str) -> None:
    """Validate Australian Business Number (ABN) format.

    Args:
        value: The ABN string to validate.

    Raises:
        ValidationError: If the ABN is not valid.

    """
    abn_pattern = r"^\d{11}$"
    if not re.match(abn_pattern, value):
        msg = "ABN must be 11 digits."
        raise ValidationError(msg)


def validate_company_name(value: str) -> None:
    """Ensure company name is not empty or whitespace only.

    Args:
        value: The company name to validate.

    Raises:
        ValidationError: If the name is empty or only whitespace.

    """
    if not value or not value.strip():
        msg = "Company name cannot be empty."
        raise ValidationError(msg)
