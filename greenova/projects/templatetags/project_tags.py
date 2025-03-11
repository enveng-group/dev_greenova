import logging
from django import template
from django.db.models import QuerySet
from typing import Dict, Any
from django.contrib.auth.models import AbstractUser
from ..models import Project, ProjectRole
from obligations.models import Obligation

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
    except Exception as e:
        logger.error(f"Error getting user role: {e}")
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
    badge_icon = {
        ProjectRole.OWNER.value: 'star',
        ProjectRole.MANAGER.value: 'cog',
        ProjectRole.MEMBER.value: 'user',
        ProjectRole.VIEWER.value: 'eye'
    }
    return {
        'role': role,
        'color': colors.get(role, 'secondary')
    }

@register.filter
def map(queryset, method_name):
    """Call a method on each object in the queryset and return a list of results"""
    if method_name == "to_dict":
        return [{"id": str(obj.id), "name": obj.name} for obj in queryset]
    return [getattr(obj, method_name)() if callable(getattr(obj, method_name)) else getattr(obj, method_name) for obj in queryset]

@register.filter
def to_list(value):
    """Convert an iterable to a list"""
    return list(value)
