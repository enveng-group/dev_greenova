from typing import Dict, List, Optional
from django.db.models import QuerySet
from .models import Obligation
from utils.constants import STATUS_CHOICES
from utils.data_utils import BaseAnalyticsProcessor, ChartDataPoint
import logging

logger = logging.getLogger(__name__)

class ObligationAnalyticsProcessor(BaseAnalyticsProcessor):
    """Obligation-specific analytics processor."""

    def __init__(self, queryset: QuerySet[Obligation], project_id: Optional[int] = None):
        super().__init__(queryset, project_id)

    def _apply_filter(self, project_id: Optional[int]) -> None:
        """Apply project-specific filtering."""
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
                "color": self.get_color(status)
            })

        # Sort by status order
        status_order = {'not started': 0, 'in progress': 1, 'completed': 2}
        data.sort(key=lambda x: status_order[x['label'].lower()])

        return {"data": data}

    def get_color(self, status: str) -> str:
        """Get color for status."""
        colors = {
            'not started': '#6c757d',
            'in progress': '#007bff',
            'completed': '#28a745',
            'overdue': '#dc3545'
        }
        return colors.get(status.lower(), '#6c757d')

    def get_completion_rate(self) -> float:
        """Calculate completion percentage."""
        total = self.queryset.count()
        if total == 0:
            return 0.0
        completed = self.queryset.filter(status='completed').count()
        return (completed / total) * 100
