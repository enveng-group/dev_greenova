"""Custom permission classes for the auditing app.

This module defines reusable, type-annotated permission classes using Django's
permissions framework and django-guardian for object-level permissions.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any

from beartype import beartype
from django.contrib.auth.models import User


@beartype
def user_can_view_auditlog(user: User, auditlog: Any) -> bool:
    """Check if the user has permission to view the audit log object.

    Args:
        user: The user instance.
        auditlog: The audit log instance.

    Returns:
        True if the user can view the audit log, False otherwise.

    """
    return user.has_perm("auditing.view_auditlog", auditlog)
