"""commons.py.

Shared logic, helpers, and base classes for the procedures app.

This module centralizes reusable code to improve maintainability and reduce duplication.
"""

from beartype import beartype


@beartype
def get_procedure_type_display(proc_type: str) -> str:
    """Return a human-readable label for a procedure type."""
    mapping = {
        "inspection": "Inspection",
        "maintenance": "Maintenance",
        "reporting": "Reporting",
        "training": "Training",
    }
    return mapping.get(proc_type, proc_type.capitalize())


# Add additional shared helpers or base classes here as needed.
