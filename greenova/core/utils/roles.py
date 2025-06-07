"""Role utilities for the core app.

Provides role display helpers for use in obligations and other apps.

Author:
    Adrian Gallo <agallo@enveng-group.com.au>

License:
    AGPL-3.0
"""


def get_role_display(role: str) -> str:
    """Return a human-readable display name for a given role string.

    Args:
        role: The role identifier.

    Returns:
        str: Human-readable role name.

    """
    return role.replace("_", " ").title()
