"""
Custom permission classes for the mechanisms app.

This module defines reusable, type-annotated permission classes using Django's
permissions framework and django-guardian for object-level permissions.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from django.contrib.auth.models import User
from typing import Any
from .types import MechanismDefinitionManager

@beartype
def user_can_view_mechanism(user: User, mechanism: Any) -> bool:
    """Check if the user has permission to view the mechanism object.

    Args:
        user: The user instance.
        mechanism: The mechanism instance.

    Returns:
        True if the user can view the mechanism, False otherwise.
    """
    return user.has_perm("mechanisms.view_mechanism", mechanism)
