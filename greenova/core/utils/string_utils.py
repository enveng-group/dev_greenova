"""String manipulation utilities for Greenova.

Provides helper functions for common string operations.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype


@beartype
def to_snake_case(text: str) -> str:
    """Convert a string to snake_case.

    Args:
        text: The input string.

    Returns:
        The snake_case version of the string.

    """
    import re

    text = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", text)
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    return text.replace("-", "_").lower()


@beartype
def truncate_string(text: str, max_length: int) -> str:
    """Truncate a string to a maximum length, adding ellipsis if needed.

    Args:
        text: The input string.
        max_length: The maximum allowed length.

    Returns:
        The truncated string.

    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
