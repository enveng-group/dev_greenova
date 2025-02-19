from django import template
from django.db.models import QuerySet
from typing import Dict, Any
from ..models import Project
from obligations.models import Obligation

register = template.Library()

@register.inclusion_tag('projects/components/tables/obligation_list.html')
def obligation_table(obligations: QuerySet[Obligation]) -> Dict[str, Any]:
    """Render obligation list table."""
    return {'obligations': obligations}

@register.filter
def get_item(dictionary: Dict[str, Any], key: Any) -> Any:
    """Get item from dictionary by key."""
    return dictionary.get(key)

@register.filter
def get_user_role(project: Any, user: Any) -> str:
    """Get user's role in project."""
    try:
        membership = project.memberships.get(user=user)
        return membership.role
    except Exception:
        return "No Role"