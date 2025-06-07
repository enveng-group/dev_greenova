"""Core utility functions and constants for Greenova.

This module provides shared logic, constants, and validators for use across all apps.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from datetime import date, timedelta
from typing import Any

from beartype import beartype
from django.core.exceptions import ValidationError
from django.utils import timezone

__all__ = [
    "get_obligation_status",
    "get_project_role_display",
    "get_responsibility_display_name",
    "is_obligation_overdue",
    "validate_non_empty_field",
    "validate_obligation_number",
    "validate_project_name",
]

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


@beartype
def validate_non_empty_field(value: str) -> None:
    """Ensure a field is not empty or whitespace only.

    Args:
        value: The string to validate.

    Raises:
        ValidationError: If the value is empty or only whitespace.

    """
    if not value or not value.strip():
        msg = "This field cannot be empty."
        raise ValidationError(msg)


@beartype
def validate_obligation_number(value: str) -> None:
    """Validate obligation number format (e.g., PCEMP-001).

    Args:
        value: The obligation number to validate.

    Raises:
        ValidationError: If the format is invalid.

    """
    import re

    if not re.match(r"^PCEMP-\d{3}$", value):
        msg = "Obligation number must be in format PCEMP-XXX."
        raise ValidationError(msg)


@beartype
def is_obligation_overdue(
    obligation: Any,
    reference_date: date | None = None,
) -> bool:
    """Determine if an obligation is overdue based on its status and due date.

    Args:
        obligation: An Obligation model instance or a dictionary with obligation attributes
        reference_date: Optional date to compare against (defaults to today)

    Returns:
        bool: True if the obligation is overdue, False otherwise

    """
    if reference_date is None:
        reference_date = timezone.now().date()
    if isinstance(obligation, dict):
        status = obligation.get("status", None)
        due_date = obligation.get("action_due_date", None)
    else:
        status = getattr(obligation, "status", None)
        due_date = getattr(obligation, "action_due_date", None)
    if status == "completed":
        return False
    if not due_date:
        return False
    return bool(due_date < reference_date)


@beartype
def get_obligation_status(obligation: Any) -> str:
    """Determine the real status of an obligation based on its due date and current status.

    Returns one of: 'overdue', 'upcoming', 'completed', or the original status.
    """
    status = getattr(obligation, "status", "").lower()
    due_date = getattr(obligation, "action_due_date", None)
    today = timezone.now().date()
    if status == "completed":
        return "completed"
    if due_date and due_date < today:
        return "overdue"
    if due_date and today <= due_date <= today + timedelta(days=14):
        return "upcoming"
    return status


@beartype
def get_responsibility_display_name(responsibility_value: str) -> str:
    """Get the display name for a responsibility value.

    Args:
        responsibility_value: The responsibility value to get display name for

    Returns:
        str: The display name for the responsibility

    """
    # Fallback: just return the input with title casing for readability
    return responsibility_value.replace("_", " ").title()
