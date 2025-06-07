"""Validators for the obligations app.

This file provides custom validators for obligation models.

Author:
    Adrian Gallo <agallo@enveng-group.com.au>

License:
    AGPL-3.0
"""

import re

from beartype import beartype
from django.core.exceptions import ValidationError


@beartype
def validate_obligation_number(value: str) -> None:
    """Validate that the obligation number matches the required format.

    Args:
        value: The obligation number to validate.

    Raises:
        ValidationError: If the format is invalid.

    """
    if not re.match(r"^PCEMP-\d+$", value):
        msg = "Obligation number must be in the format PCEMP-XXX where XXX is a number"
        raise ValidationError(
            msg,
        )
