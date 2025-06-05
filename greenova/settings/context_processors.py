"""Custom context processors for the settings app.

Provides application/user settings, feature toggles, or preferences for templates.

Returns:
    dict: Context variables for templates.
"""
from typing import Any, Dict
from beartype import beartype
from django.conf import settings as django_settings

@beartype
def settings_context(request) -> Dict[str, Any]:
    """Inject settings-related context variables into templates.

    Args:
        request: The current HttpRequest object.

    Returns:
        A dictionary of settings-related context variables, including:
            - user_settings: Dict of user-specific settings or preferences.
            - system_settings: Dict of system-wide settings.
            - theme_preference: User's theme preference (e.g., 'light', 'dark').
    """
    user_settings = {}
    theme_preference = None
    if hasattr(request, "user") and request.user.is_authenticated:
        # Example: get user settings from profile or session
        user_settings = getattr(request.user, "profile", {})
        theme_preference = getattr(request.user, "theme_preference", None)
    if not theme_preference:
        theme_preference = request.session.get("theme_preference", "light")
    # Example: system settings from Django settings
    system_settings = {
        "site_name": getattr(django_settings, "SITE_NAME", "Greenova"),
        "site_version": getattr(django_settings, "SITE_VERSION", "1.0.0"),
        "feature_flags": getattr(django_settings, "FEATURE_FLAGS", {}),
    }
    return {
        "user_settings": user_settings,
        "system_settings": system_settings,
        "theme_preference": theme_preference,
    }
