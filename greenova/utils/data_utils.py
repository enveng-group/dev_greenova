from typing import Dict, List, TypedDict, Optional, Any
from datetime import date
from django.db.models import QuerySet
from obligations.models import Obligation
from utils.constants import STATUS_CHOICES
import logging
from .serializers import ChartDataSerializer
from .exceptions import ChartDataError

logger = logging.getLogger(__name__)

class ChartDataPoint(TypedDict):
    label: str
    value: int
    color: str

class TimeSeriesPoint(TypedDict):
    date: date
    count: int
    status: str

class AnalyticsDataProcessor:
    """Process data for analytics visualizations."""

    def __init__(self, queryset: QuerySet[Obligation], project_id: Optional[int] = None) -> None:
        self.queryset = queryset
        if project_id:
            self.queryset = self.queryset.filter(project_id=project_id)

    def get_mechanism_data(self, mechanism_name: str = "all") -> Dict[str, List[ChartDataPoint]]:
        """Get status distribution for a mechanism."""
        queryset = self.queryset
        if mechanism_name != "all":
            queryset = queryset.filter(primary_environmental_mechanism=mechanism_name)

        data: List[ChartDataPoint] = []
        for status, _ in STATUS_CHOICES:
            count = queryset.filter(status=status).count()
            data.append({
                "label": status.title(),
                "value": count,
                "color": self._get_status_color(status)
            })
        return {"data": data}

    def _get_status_color(self, status: str) -> str:
        """Get color for status."""
        colors = {
            'not started': '#6c757d',
            'in progress': '#007bff',
            'completed': '#28a745',
            'overdue': '#dc3545'
        }
        return colors.get(status.lower(), '#6c757d')

    def _calculate_completion_rate(self) -> float:
        """Calculate completion percentage."""
        total = self.queryset.count()
        if total == 0:
            return 0.0
        completed = self.queryset.filter(status='completed').count()
        return (completed / total) * 100

    def get_chart_data(self, mechanism_name: str = "all") -> Dict[str, Any]:
        """Get formatted chart data."""
        try:
            data = self.get_mechanism_data(mechanism_name)
            return ChartDataSerializer.format_mechanism_data(data['data'])
        except Exception as e:
            raise ChartDataError(f"Error processing chart data: {str(e)}")
