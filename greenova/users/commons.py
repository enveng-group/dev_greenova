"""commons.py.

Shared logic, helpers, and base classes for the users app.

This module centralizes reusable code to improve maintainability and reduce duplication.
"""

from beartype import beartype


@beartype
def is_superuser_or_staff(user) -> bool:
    """Return True if the user is a superuser or staff."""
    return getattr(user, "is_superuser", False) or getattr(user, "is_staff", False)


# Add additional shared helpers or base classes here as needed.
