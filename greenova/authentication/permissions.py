"""
Custom permission classes for the authentication app.

This module defines reusable, type-annotated permission classes using Django's
permissions framework and django-guardian for object-level permissions.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from django.contrib.auth.models import User
from typing import Any
from .types import PermissionChecker

@beartype
def user_can_manage_auth(user: User, obj: Any) -> bool:
    """Check if the user has permission to manage authentication-related objects.

    Args:
        user: The user instance.
        obj: The authentication-related object (e.g., MFA device, session).

    Returns:
        True if the user can manage the object, False otherwise.
    """
    return user.has_perm("authentication.manage_auth", obj)
