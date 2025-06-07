"""commons.py.

Shared logic, helpers, and base classes for the responsibility app.

This module centralizes reusable code to improve maintainability and reduce duplication.
"""

from beartype import beartype


@beartype
def get_responsibility_type_display(res_type: str) -> str:
    """Return a human-readable label for a responsibility type."""
    mapping = {
        "primary": "Primary",
        "secondary": "Secondary",
        "tertiary": "Tertiary",
    }
    return mapping.get(res_type, res_type.capitalize())


# Add additional shared helpers or base classes here as needed.
