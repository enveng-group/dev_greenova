"""Custom context processors for the authentication app.

Provides user/session info and authentication-related context for templates.

Returns:
    dict: Context variables for templates.
"""
from typing import Any, Dict
from beartype import beartype
from django.utils import timezone
from django.conf import settings
from allauth.mfa.models import Authenticator

@beartype
def authentication_context(request) -> Dict[str, Any]:
    """Inject authentication-related context variables into templates.

    Args:
        request: The current HttpRequest object.

    Returns:
        A dictionary of authentication-related context variables, including:
            - user: The current user object.
            - is_authenticated: Whether the user is authenticated.
            - mfa_enabled: Whether MFA is enabled for the user.
            - session_expiry: Session expiry datetime (UTC) or None.
    """
    user = getattr(request, "user", None)
    is_authenticated = getattr(user, "is_authenticated", False)
    mfa_enabled = False
    if is_authenticated and hasattr(user, "pk"):
        mfa_enabled = Authenticator.objects.filter(user=user, confirmed=True).exists()
    session_expiry = None
    if hasattr(request, "session") and hasattr(request.session, "get_expiry_date"):
        session_expiry = request.session.get_expiry_date()
    return {
        "user": user,
        "is_authenticated": is_authenticated,
        "mfa_enabled": mfa_enabled,
        "session_expiry": session_expiry,
    }
