"""commons.py.

Shared logic, helpers, and base classes for the mechanisms app.

This module centralizes reusable code to improve maintainability and reduce duplication.
"""

from beartype import beartype
from .types import MechanismDefinitionDict, MechanismStateDict

MECHANISM_STATUS_COLORS = {
    "Active": "#43aa8b",
    "Inactive": "#f9c74f",
    "Archived": "#b0b0b0",
}


@beartype
def get_mechanism_type_display(mechanism_type: str) -> str:
    """Return a human-readable label for a mechanism type."""
    mapping = {
        "physical": "Physical",
        "administrative": "Administrative",
        "technical": "Technical",
    }
    return mapping.get(mechanism_type, mechanism_type.capitalize())


# Add additional shared helpers or base classes here as needed.
