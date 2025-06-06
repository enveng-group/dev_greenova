"""Core utility functions and constants for Greenova.

This module provides shared logic, constants, and validators for use across all apps.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from django.core.exceptions import ValidationError

# --- Constants (migrated from projects/constants.py) ---
ROLE_OWNER = "owner"
ROLE_MANAGER = "manager"
ROLE_MEMBER = "member"
ROLE_VIEWER = "viewer"

PROJECT_ROLE_CHOICES = [
    (ROLE_OWNER, "Owner"),
    (ROLE_MANAGER, "Manager"),
    (ROLE_MEMBER, "Member"),
    (ROLE_VIEWER, "Viewer"),
]


@beartype
def get_project_role_display(role: str) -> str:
    """Return a human-readable label for a project role."""
    mapping = {
        ROLE_OWNER: "Owner",
        ROLE_MANAGER: "Manager",
        ROLE_MEMBER: "Member",
        ROLE_VIEWER: "Viewer",
    }
    return mapping.get(role, role.capitalize())


@beartype
def validate_project_name(value: str) -> None:
    """Ensure project name is not empty or whitespace only.

    Args:
        value: The project name to validate.

    Raises:
        ValidationError: If the name is empty or only whitespace.

    """
    if not value or not value.strip():
        msg = "Project name cannot be empty."
        raise ValidationError(msg)
