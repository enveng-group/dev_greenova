"""Global permission utilities for Greenova.

Reusable permission checks for use across all apps.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any

from beartype import beartype
from django.contrib.auth.models import User


@beartype
def user_can_view_project(user: User, project: Any) -> bool:
    """Check if the user has permission to view the project object.

    Args:
        user: The user instance.
        project: The project instance.

    Returns:
        True if the user can view the project, False otherwise.

    """
    return user.has_perm("projects.view_project", project)


@beartype
def user_can_view_obligation(user: User, obligation: Any) -> bool:
    """Check if the user has permission to view the obligation object.

    Args:
        user: The user instance.
        obligation: The obligation instance.

    Returns:
        True if the user can view the obligation, False otherwise.

    """
    return user.has_perm("obligations.view_obligation", obligation)


@beartype
def user_can_view_mechanism(user: User, mechanism: Any) -> bool:
    """Check if the user has permission to view the mechanism object.

    Args:
        user: The user instance.
        mechanism: The mechanism instance.

    Returns:
        True if the user can view the mechanism, False otherwise.

    """
    return user.has_perm("mechanisms.view_environmentalmechanism", mechanism)
