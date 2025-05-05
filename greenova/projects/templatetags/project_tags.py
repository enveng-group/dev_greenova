import logging
from typing import Any, Dict, List, Optional

from django import template
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.utils.html import format_html
from obligations.models import Obligation

from ..models import Project, ProjectRole

logger = logging.getLogger(__name__)

register = template.Library()

@register.inclusion_tag('obligations/components/tables/obligation_list.html')
def obligation_table(obligations: QuerySet[Obligation]) -> Dict[str, Any]:
    """Render obligation list table."""
    return {'obligations': obligations}

@register.filter
def get_item(dictionary: Dict[str, Any], key: Any) -> Any:
    """Get item from dictionary by key."""
    return dictionary.get(key)

@register.filter
def get_user_role(project: Project, user: AbstractUser) -> str:
    """
    Get user's role in project.

    Args:
        project: The project to check
        user: The user to get role for

    Returns:
        str: User's role or 'viewer' if none found
    """
    try:
        return project.get_user_role(user)
    except ObjectDoesNotExist as e:
        logger.error("Error getting user role: %s", str(e))
        return ProjectRole.VIEWER.value

@register.filter
def format_role(role: str) -> str:
    """Format role name for display."""
    return role.replace('_', ' ').title()

@register.inclusion_tag('projects/components/role_badge.html')
def role_badge(role: str) -> Dict[str, str]:
    """Render role badge."""
    colors = {
        ProjectRole.OWNER.value: 'primary',
        ProjectRole.MANAGER.value: 'success',
        ProjectRole.MEMBER.value: 'info',
        ProjectRole.VIEWER.value: 'secondary'
    }
    return {
        'role': role,
        'color': colors.get(role, 'secondary')
    }

@register.filter
def transform_queryset(queryset, method_name):
    """Call a method on each object in the queryset and return a list of results"""
    if method_name == "to_dict":
        return [{"id": str(obj.id), "name": obj.name} for obj in queryset]
    return [
        getattr(obj, method_name)()
        if callable(getattr(obj, method_name))
        else getattr(obj, method_name)
        for obj in queryset
    ]

@register.filter
def to_list(value):
    """Convert an iterable to a list"""
    return list(value)

@register.simple_tag
def project_status_badge(status: str) -> str:
    """Generate a status badge for projects."""
    status_classes = {
        'active': 'bg-green-100 text-green-800',
        'pending': 'bg-yellow-100 text-yellow-800',
        'completed': 'bg-blue-100 text-blue-800',
        'cancelled': 'bg-red-100 text-red-800',
    }

    css_class = status_classes.get(status.lower(), 'bg-gray-100 text-gray-800')

    return format_html(
        '<span class="badge {}">{}</span>',
        css_class,
        status.title()
    )

@register.simple_tag
def project_badge(project_type: str, display_text: Optional[str] = None) -> str:
    """Generate a badge for project types with icon and text."""
    try:
        badge_config = get_badge_config(project_type)
    except ValueError as e:
        logger.error('Error generating project badge: %s', str(e))
        return ''

    return format_html(
        '<span class="inline-flex items-center px-3 py-0.5 '
        'rounded-full text-sm font-medium {}">{}</span>',
        badge_config['css_class'],
        display_text or project_type.title()
    )

def get_badge_config(project_type: str) -> Dict[str, str]:
    """Get badge configuration for a project type."""
    badge_configs = {
        'environmental': {
            'css_class': 'bg-green-100 text-green-800',
        },
        'compliance': {
            'css_class': 'bg-blue-100 text-blue-800',
        },
        'monitoring': {
            'css_class': 'bg-yellow-100 text-yellow-800',
        },
    }

    config = badge_configs.get(project_type.lower())
    if not config:
        raise ValueError(f'Unsupported project type: {project_type}')

    return config

@register.inclusion_tag('projects/partials/project_list.html')
def project_list(projects: List[Any], max_items: int = 5) -> Dict[str, Any]:
    """Render a list of projects."""
    return {
        'projects': projects[:max_items],
    }
