"""
Custom permission classes for the reports app.

This module defines reusable, type-annotated permission classes using Django's
permissions framework and django-guardian for object-level permissions.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from django.contrib.auth.models import User
from typing import Any
from .types import ReportPayloadManager, ExportFormatter

@beartype
def user_can_view_report(user: User, report: Any) -> bool:
    """Check if the user has permission to view the report object.

    Args:
        user: The user instance.
        report: The report instance.

    Returns:
        True if the user can view the report, False otherwise.
    """
    return user.has_perm("reports.view_report", report)
