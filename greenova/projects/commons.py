"""commons.py.

Shared logic, helpers, and base classes for the projects app.

This module centralizes reusable code to improve maintainability and reduce duplication.
"""

from beartype import beartype


@beartype
def get_project_role_display(role: str) -> str:
    """Return a human-readable label for a project role."""
    mapping = {
        "owner": "Owner",
        "manager": "Manager",
        "member": "Member",
        "viewer": "Viewer",
    }
    return mapping.get(role, role.capitalize())


# Add additional shared helpers or base classes here as needed.
