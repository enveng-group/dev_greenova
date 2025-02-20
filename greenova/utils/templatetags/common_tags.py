from django import template
from django.utils.safestring import mark_safe
from typing import Any, Dict
from django.contrib.auth.models import User
from projects.models import Project
from utils.commons import get_status_badge, get_user_display_name, get_project_stats

register = template.Library()

@register.filter
def status_badge(value: str) -> str:
    """Render a status badge with appropriate styling."""
    return mark_safe(get_status_badge(value))

@register.filter
def display_name(user: User) -> str:
    """Return the best display name for a user."""
    return get_user_display_name(user)

@register.simple_tag
def project_stats(project: Project) -> Dict[str, Any]:
    """Return project statistics."""
    return get_project_stats(project)

@register.filter
def format_error(error: str) -> str:
    """Format error messages consistently."""
    return mark_safe(f'<p class="error-message">{error}</p>')

@register.simple_tag
def system_status() -> Dict[str, str]:
    """Get system status information."""
    from django.conf import settings
    return {
        'status': settings.SYSTEM_STATUS,
        'version': settings.APP_VERSION,
        'environment': settings.ENVIRONMENT_NAME
    }

@register.filter
def json_script(value: Any) -> str:
    """Safely serialize value to JSON for use in scripts."""
    import json
    from django.utils.safestring import mark_safe
    return mark_safe(json.dumps(value))

    
