"""
Custom permission classes for the users app.

This module defines reusable, type-annotated permission classes using Django's
permissions framework and django-guardian for object-level permissions.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from django.contrib.auth.models import User
from typing import Any
from .types import UserProfileManager, PermissionManager

@beartype
def user_can_view_user(user: User, target_user: Any) -> bool:
    """Check if the user has permission to view the target user object.

    Args:
        user: The user instance.
        target_user: The user instance being accessed.

    Returns:
        True if the user can view the target user, False otherwise.
    """
    return user.has_perm("users.view_user", target_user)
