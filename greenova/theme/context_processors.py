"""Custom context processors for the theme app.

Provides theme/branding info for templates (if dynamic theming/branding is used).

Returns:
    dict: Context variables for templates.
"""
from typing import Any, Dict
from beartype import beartype
from django.conf import settings as django_settings

@beartype
def theme_context(request) -> Dict[str, Any]:
    """Inject theme/branding context variables into templates.

    Args:
        request: The current HttpRequest object.

    Returns:
        A dictionary of theme/branding context variables, including:
            - theme: The current theme name (e.g., 'light', 'dark').
            - brand_logo: URL to the brand logo image.
            - primary_color: Primary brand color (hex or CSS var).
            - secondary_color: Secondary brand color (hex or CSS var).
    """
    theme = request.session.get("theme_preference") or getattr(request.user, "theme_preference", None) or "light"
    brand_logo = getattr(django_settings, "BRAND_LOGO_URL", "/static/img/brand-logo.png")
    primary_color = getattr(django_settings, "PRIMARY_COLOR", "#2563eb")  # Tailwind blue-600
    secondary_color = getattr(django_settings, "SECONDARY_COLOR", "#f59e42")  # Tailwind orange-400
    return {
        "theme": theme,
        "brand_logo": brand_logo,
        "primary_color": primary_color,
        "secondary_color": secondary_color,
    }
