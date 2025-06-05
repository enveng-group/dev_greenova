"""
Custom permission classes for the projects app.

This module defines reusable, type-annotated permission classes using Django's
permissions framework and django-guardian for object-level permissions.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from django.contrib.auth.models import User
from typing import Any
from .types import ProjectManager, MembershipManager

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
