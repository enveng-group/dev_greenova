from django import template
from typing import Dict, Any
from django.db.models import QuerySet
from obligations.models import Obligation
from projects.models import Project
from utils.data_utils import AnalyticsDataProcessor

register = template.Library()

@register.simple_tag
def mechanism_chart_data(mechanism: str) -> Dict[str, Any]:
    """Get chart data for mechanism."""
    queryset = Obligation.objects.filter(
        primary_environmental_mechanism=mechanism
    ).all()
    processor = AnalyticsDataProcessor(queryset)
    return processor.get_mechanism_data(mechanism)

@register.simple_tag
def aspect_chart_data(project_id: int, aspect: str) -> Dict[str, Any]:
    """Get chart data for environmental aspect analysis."""
    try:
        project = Project.objects.get(id=project_id)
        # Use direct Obligation query instead
        obligations = Obligation.objects.filter(
            project=project,
            environmental_aspect=aspect
        )
        processor = AnalyticsDataProcessor(obligations)
        return processor.get_mechanism_data(aspect)
    except Project.DoesNotExist:
        return {}

@register.inclusion_tag('analytics/components/charts/trend_chart.html')
def trend_chart(days: int = 30) -> Dict[str, Any]:
    """Render trend chart."""
    from datetime import datetime, timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    processor = AnalyticsDataProcessor(Obligation.objects.all())
    return {
        'data': processor.get_time_series_data(start_date, end_date)
    }

@register.inclusion_tag('analytics/components/charts/aspect_analysis_chart.html')
def aspect_analysis_chart(project: Project, aspect: str) -> Dict[str, Any]:
    """Render aspect analysis chart."""
    return {
        'project': project,
        'aspect': aspect,
        'chart_data': aspect_chart_data(project.id, aspect)
    }

@register.filter
def completion_rate(queryset: QuerySet[Obligation]) -> float:
    """Calculate completion rate for a queryset of obligations."""
    total = queryset.count()
    if total == 0:
        return 0.0
    completed = queryset.filter(status='completed').count()
    return (completed / total) * 100