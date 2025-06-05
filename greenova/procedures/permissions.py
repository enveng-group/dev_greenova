"""
Custom permission classes for the procedures app.

This module defines reusable, type-annotated permission classes using Django's
permissions framework and django-guardian for object-level permissions.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from django.contrib.auth.models import User
from typing import Any
from .types import ProcedureStepDict, ProcedureManager

@beartype
def user_can_view_procedure(user: User, procedure: Any) -> bool:
    """Check if the user has permission to view the procedure object.

    Args:
        user: The user instance.
        procedure: The procedure instance.

    Returns:
        True if the user can view the procedure, False otherwise.
    """
    return user.has_perm("procedures.view_procedure", procedure)
