"""Helper functions for managing audit logs in Greenova.

Provides utility functions to simplify audit log creation and management.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from datetime import datetime

from beartype import beartype
from django.utils.timezone import now


@beartype
def format_audit_message(
    user: str | None,
    action: str,
    object_type: str,
    object_id: str,
    message: str,
) -> str:
    """Format a standardized audit log message.

    Args:
        user: The username of the user performing the action.
        action: The action being logged (e.g., 'created', 'updated').
        object_type: The type of object being acted upon.
        object_id: The ID of the object being acted upon.
        message: A detailed message describing the action.

    Returns:
        A formatted string for the audit log.

    """
    timestamp = now().isoformat()
    user_info = f"User: {user}" if user else "System"
    return (
        f"[{timestamp}] {user_info} | Action: {action} | Object: "
        f"{object_type}({object_id}) | {message}"
    )


@beartype
def create_audit_log_entry(
    user_id: int,
    action: str,
    details: str,
) -> dict[str, str | int | datetime]:
    """Create a dictionary representing an audit log entry.

    Args:
        user_id: The ID of the user performing the action.
        action: The action performed.
        details: Additional details about the action.

    Returns:
        dict: A dictionary representing the audit log entry.

    """
    return {
        "user_id": user_id,
        "action": action,
        "details": details,
        "timestamp": now(),
    }
