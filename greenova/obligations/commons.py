"""commons.py.

Shared logic, helpers, and base classes for the obligations app.

This module centralizes reusable code to improve maintainability and reduce duplication.
"""

from beartype import beartype

OBLIGATION_STATUS_CHOICES = [
    ("not_started", "Not Started"),
    ("in_progress", "In Progress"),
    ("completed", "Completed"),
    ("overdue", "Overdue"),
]


@beartype
def normalize_frequency(freq: str) -> str:
    """Normalize frequency string to a canonical value.

    Args:
        freq: The frequency string to normalize.

    Returns:
        The canonical frequency string.

    """
    mapping = {
        "annual": "Annual",
        "biannual": "Biannual",
        "monthly": "Monthly",
        "quarterly": "Quarterly",
        "weekly": "Weekly",
        "daily": "Daily",
    }
    return mapping.get(freq.lower(), freq.capitalize())


# Add additional shared helpers or base classes here as needed.
