"""
Custom permission classes for the dashboard app.

This module defines reusable, type-annotated permission classes using Django's
permissions framework and django-guardian for object-level permissions.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from django.contrib.auth.models import User
from typing import Any

@beartype
def user_can_view_dashboard(user: User) -> bool:
    """Check if the user has permission to view the dashboard.

    Args:
        user: The user instance.

    Returns:
        True if the user can view the dashboard, False otherwise.
    """
    return user.has_perm("dashboard.view_dashboard")
