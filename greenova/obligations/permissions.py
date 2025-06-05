"""
Custom permission classes for the obligations app.

This module defines reusable, type-annotated permission classes using Django's
permissions framework and django-guardian for object-level permissions.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from django.contrib.auth.models import User
from typing import Any
from .types import ObligationDataDict, ComplianceStatusDict, ComplianceChecker

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
