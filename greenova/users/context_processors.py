"""Custom context processors for the users app.

Provides user profile info, notifications, or preferences for templates.

Returns:
    dict: Context variables for templates.
"""
from typing import Any, Dict
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from beartype import beartype

@beartype
def users_context(request) -> Dict[str, Any]:
    """Inject user profile and permission context variables into templates.

    Args:
        request: The current HttpRequest object.

    Returns:
        A dictionary of user context variables, including:
            - user_profile: The user profile object or None.
            - user_permissions: Set of permission codenames for the user.
            - is_admin: Boolean, True if user is staff or superuser.
    """
    user = getattr(request, "user", None)
    user_profile = None
    user_permissions = set()
    is_admin = False
    if user and user.is_authenticated:
        user_profile = user
        user_permissions = set(user.get_all_permissions())
        is_admin = user.is_staff or user.is_superuser
    return {
        "user_profile": user_profile,
        "user_permissions": user_permissions,
        "is_admin": is_admin,
    }
