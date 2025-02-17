from django import template
from typing import Dict, Any
from projects.models import Obligation
from analytics.data_utils import AnalyticsDataProcessor

register = template.Library()

@register.simple_tag
def mechanism_chart_data(mechanism: str) -> Dict[str, Any]:
    """Get chart data for mechanism."""
    processor = AnalyticsDataProcessor(
        Obligation.objects.filter(
            primary_environmental_mechanism=mechanism
        )
    )
    return processor.get_mechanism_data(mechanism)

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