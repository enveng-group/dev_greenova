from django import template
from beartype import beartype

register = template.Library()


@register.simple_tag
@beartype
def get_theme(theme: str | None = None) -> str:
    """Return the current theme or 'light'.

    Args:
        theme: The theme string or None.

    Returns:
        The current theme or 'light' if not set.
    """
    return theme or "light"


@register.simple_tag
@beartype
def get_brand_logo(brand_logo: str | None = None) -> str:
    """Return the brand logo URL or a default.

    Args:
        brand_logo: The brand logo URL or None.

    Returns:
        The brand logo URL or a default.
    """
    return brand_logo or "/static/img/brand-logo.png"


@register.simple_tag
@beartype
def get_primary_color(primary_color: str | None = None) -> str:
    """Return the primary color or a default.

    Args:
        primary_color: The primary color string or None.

    Returns:
        The primary color or a default.
    """
    return primary_color or "#2563eb"


@register.simple_tag
@beartype
def get_secondary_color(secondary_color: str | None = None) -> str:
    """Return the secondary color or a default.

    Args:
        secondary_color: The secondary color string or None.

    Returns:
        The secondary color or a default.
    """
    return secondary_color or "#f59e42"
