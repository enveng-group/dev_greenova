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
        The string converted to snake_case.

    """
    import re

    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()


@beartype
def truncate_string(text: str, max_length: int) -> str:
    """Truncate a string to a maximum length, adding ellipsis if necessary.

    Args:
        text: The input string.
        max_length: The maximum allowed length.

    Returns:
        The truncated string.

    """
    return text if len(text) <= max_length else text[: max_length - 3] + "..."
