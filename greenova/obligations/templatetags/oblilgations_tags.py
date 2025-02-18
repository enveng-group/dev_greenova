from django import template
from typing import Dict, Any
from projects.models import Project
from django.db.models import QuerySet

register = template.Library()

@register.simple_tag
def obligation_stats(project: Project) -> Dict[str, int]:
    """Return obligation statistics for a project."""
    return {
        'total': project.obligations.count(),
        'completed': project.get_completed_obligations().count(),
        'active': project.get_active_obligations().count(),
        'overdue': project.get_overdue_obligations().count()
    }

@register.inclusion_tag('obligations/components/obligation_summary.html')
def obligation_summary(project: Project) -> Dict[str, Any]:
    """Render obligation summary."""
    return {'stats': obligation_stats(project)}

@register.filter
def status_class(status: str) -> str:
    """Return CSS class for obligation status."""
    status_classes = {
        'not started': 'status-not-started',
        'in progress': 'status-in-progress',
        'completed': 'status-completed',
        'overdue': 'status-overdue'
    }
    return status_classes.get(status.lower(), '')