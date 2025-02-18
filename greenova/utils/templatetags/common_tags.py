from django import template
from django.utils.safestring import mark_safe
from typing import Any, Dict

register = template.Library()

@register.filter
def status_badge(value: str) -> str:
    """Render a status badge with appropriate styling."""
    colors = {
        'not started': 'var(--error)',
        'in progress': 'var(--primary)',
        'completed': 'var(--success)'
    }
    return mark_safe(
        f'<mark data-status="{value}" '
        f'style="background-color: {colors.get(value, "var(--muted)")}">'
        f'{value.title()}</mark>'
    )

@register.filter
def format_error(error: str) -> str:
    """Format error messages with consistent styling."""
    return mark_safe(f'<mark class="error" role="alert">{error}</mark>')

@register.simple_tag
def system_info() -> Dict[str, Any]:
    """Return system information for footer."""
    from django.conf import settings
    return {
        'version': getattr(settings, 'APP_VERSION', '0.1.0'),
        'status': 'operational',
        'environment': getattr(settings, 'ENVIRONMENT', 'development')
    }

@register.simple_tag
def chart_error_message() -> str:
    """Return standard chart error message."""
    return "Unable to load chart data. Please try again later."

@register.filter
def json_script(value: Any) -> str:
    """Safely encode data as JSON for use in scripts."""
    import json
    return mark_safe(json.dumps(value))