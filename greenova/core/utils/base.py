"""Core utility functions and constants for Greenova.

This module provides shared logic, constants, and validators for use across all apps.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from collections.abc import Mapping
from datetime import date
from typing import Any, cast

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
def get_obligation_status(due_date: date, is_complete: bool) -> str:
    """Return obligation status based on due date and completion flag."""
    if is_complete:
        return "completed"
    today = date.today()
    if due_date < today:
        return "overdue"
    if due_date == today:
        return "in progress"
    return "upcoming"


@beartype
def get_project_role_display(role: str) -> str:
    """Return display string for a project role."""
    return role.replace("_", " ").title()


@beartype
def validate_project_name(value: str) -> None:
    """Validate project name (must be non-empty and at least 3 chars)."""
    if not value or len(value.strip()) < 3:
        msg = "Project name must be at least 3 characters."
        raise ValidationError(msg)


@beartype
def validate_non_empty_field(value: Any) -> None:
    """Raise ValidationError if value is empty."""
    if not value:
        msg = "This field cannot be empty."
        raise ValidationError(msg)


@beartype
def validate_obligation_number(value: str) -> None:
    """Validate obligation number format (must be non-empty and alphanumeric)."""
    if not value or not value.isalnum():
        msg = "Obligation number must be alphanumeric."
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
        status = get_status_from_obligation(obligation)
        due_date = get_due_date_from_obligation(obligation)
    else:
        status = getattr(obligation, "status", None)
        due_date = getattr(obligation, "action_due_date", None)
    if status == "completed":
        return False
    if not due_date:
        return False
    return bool(due_date < reference_date)


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


@beartype
def get_status_from_obligation(obligation: Mapping[str, Any]) -> str | None:
    """Get the status from an obligation dict.

    Args:
        obligation: The obligation dictionary.

    Returns:
        The status string or None.

    """
    status = obligation.get("status", None)
    return cast("str | None", status)


@beartype
def get_due_date_from_obligation(obligation: Mapping[str, Any]) -> Any:
    """Get the due date from an obligation dict.

    Args:
        obligation: The obligation dictionary.

    Returns:
        The due date value or None.

    """
    return obligation.get("action_due_date", None)
