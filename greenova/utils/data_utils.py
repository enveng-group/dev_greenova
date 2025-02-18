import logging
from typing import Dict, List, TypedDict, Any
from datetime import datetime, date
from django.db.models import QuerySet, Count
from obligations.models import Obligation
from utils.constants import STATUS_CHOICES

logger = logging.getLogger(__name__)

class ChartDataError(Exception):
    """Exception raised for errors in chart data processing."""
    pass

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
    
    def __init__(self, queryset: QuerySet[Obligation]) -> None:
        self.queryset = queryset

    def get_mechanism_data(self, mechanism: str) -> Dict[str, List[Any]]:
        """Get status distribution for a mechanism."""
        try:
            status_counts = (
                self.queryset
                .filter(primary_environmental_mechanism=mechanism)
                .values('status')
                .annotate(count=Count('status'))
                .order_by('status')
            )
            
            data: Dict[str, List[Any]] = {
                'labels': [status[1] for status in STATUS_CHOICES],
                'values': [0] * len(STATUS_CHOICES),
                'colors': ['var(--error)', 'var(--primary)', 'var(--success)']
            }
            
            status_map = {status[0]: i for i, status in enumerate(STATUS_CHOICES)}
            for item in status_counts:
                idx = status_map.get(item['status'])
                if idx is not None:
                    data['values'][idx] = item['count']
                    
            return data
        except Exception as e:
            logger.error(f"Error processing mechanism data: {str(e)}")
            raise ChartDataError("Failed to process mechanism data")

    def get_time_series_data(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[TimeSeriesPoint]:
        """Get time series data for trend analysis."""
        query_result = (
            self.queryset
            .filter(
                action_due_date__range=(start_date, end_date)
            )
            .values('action_due_date', 'status')
            .annotate(count=Count('id'))
            .order_by('action_due_date')
        )
        
        return [
            TimeSeriesPoint(
                date=item['action_due_date'],
                count=item['count'],
                status=item['status']
            ) for item in query_result
        ]