"""
Custom permission classes for the company app.

This module defines reusable, type-annotated permission classes using Django's
permissions framework and django-guardian for object-level permissions.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from django.contrib.auth.models import User
from typing import Any
from .types import CompanyProfileManager

@beartype
def user_can_view_company(user: User, company: Any) -> bool:
    """Check if the user has permission to view the company object.

    Args:
        user: The user instance.
        company: The company instance.

    Returns:
        True if the user can view the company, False otherwise.
    """
    return user.has_perm("company.view_company", company)


@beartype
def user_can_edit_company(user: User, company: Any) -> bool:
    """Check if the user has permission to edit the company object.

    Args:
        user: The user instance.
        company: The company instance.

    Returns:
        True if the user can edit the company, False otherwise.
    """
    return user.has_perm("company.change_company", company)
