from django import template
from django.contrib.auth import get_user_model
from projects.models import Project
from typing import Dict, Any  # Add import

register = template.Library()

@register.filter
def display_name(user) -> str:
    """Return the best display name for a user."""
    return user.get_full_name() or user.username

@register.simple_tag
def project_stats(project: Project) -> Dict[str, int]:
    """Return project statistics."""
    return {
        'total': project.obligations.count(),
        'completed': project.get_completed_obligations().count(),
        'active': project.get_active_obligations().count(),
        'overdue': project.get_overdue_obligations().count()
    }

@register.inclusion_tag('dashboard/components/charts/obligation_summary.html')
def obligation_summary(project: Project) -> Dict[str, Any]:
    """Render obligation summary chart."""
    return {'stats': project_stats(project)}