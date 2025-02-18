from django import template
from django.db.models import QuerySet
from typing import Dict, Any
from ..models import Project
from obligations.models import Obligation

register = template.Library()

@register.inclusion_tag('projects/components/charts/project_stats.html')
def project_stats_chart(project: Project) -> Dict[str, Any]:
    """Render project statistics chart."""
    return {
        'stats': {
            'total': project.obligations.count(),
            'completed': project.get_completed_obligations().count(),
            'active': project.get_active_obligations().count(),
            'overdue': project.get_overdue_obligations().count()
        }
    }

@register.inclusion_tag('projects/components/tables/obligation_list.html')
def obligation_table(obligations: QuerySet[Obligation]) -> Dict[str, Any]:
    """Render obligation list table."""
    return {'obligations': obligations}