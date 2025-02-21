from django import template
from django.utils.safestring import mark_safe
from typing import Any, Dict, Optional, List
from django.contrib.auth.models import User
from projects.models import Project
from utils.commons import get_status_badge, get_user_display_name, get_project_stats
from django.db.models import QuerySet

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

@register.inclusion_tag('components/charts/chart_container.html')
def chart_container(
    chart_id: str,
    title: str,
    data: Dict[str, Any],
    description: Optional[str] = None,
    height: str = "300px",
    htmx_url: Optional[str] = None,
    htmx_trigger: str = "load",
    htmx_swap: str = "none",
    stats: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Render a standardized chart container."""
    return {
        'chart_id': chart_id,
        'chart_title': title,
        'chart_data': data,
        'chart_description': description,
        'height': height,
        'htmx_url': htmx_url,
        'htmx_trigger': htmx_trigger,
        'htmx_swap': htmx_swap,
        'chart_stats': stats
    }

@register.inclusion_tag('components/data_table.html')
def data_table(data: QuerySet, headers: List[str], title: str, empty_message: Optional[str] = None) -> Dict[str, Any]:
    return {
        'data': data,
        'headers': headers,
        'title': title,
        'empty_message': empty_message
    }

@register.inclusion_tag('components/dialogs/base_dialog.html')
def modal_dialog(dialog_id: str, title: str, content_template: str, **kwargs) -> Dict[str, Any]:
    """Render a modal dialog."""
    return {
        'dialog_id': dialog_id,
        'title': title,
        'content_template': content_template,
        **kwargs
    }
