from typing import Any, Dict, Optional, TypedDict, List
from django.http import HttpRequest
from django.db.models import QuerySet
from projects.models import Obligation
from utils.logger import log_action

class DataPoint(TypedDict):
    name: str
    value: int
    status: str

class DataStructure(TypedDict):
    name: str
    value: int
    status: str
    format: str
    count: int
    data: List[Dict[str, Any]]

class AnalyticsActions:
    """Handle analytics-related actions."""

    @staticmethod
    @log_action("Export analytics data")
    def export_data(
        request: HttpRequest,
        queryset: QuerySet[Obligation],
        format: str = 'csv'
    ) -> Dict[str, Any]:
        """Export analytics data in specified format."""
        try:
            data: Dict[str, Any] = {
                'format': format,
                'count': queryset.count(),
                'data': list(queryset.values())
            }
            return data
        except Exception as e:
            raise ValueError(f"Export failed: {str(e)}")

    @staticmethod
    @log_action("Generate performance report")
    def generate_report(
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, str]:
        """Generate performance report for date range."""
        try:
            return {
                'start_date': start_date or '',
                'end_date': end_date or '',
                'status': 'generated'
            }
        except Exception as e:
            raise ValueError(f"Report generation failed: {str(e)}")

    @staticmethod
    @log_action("Calculate analytics metrics")
    def calculate_metrics(
        queryset: QuerySet[Obligation]
    ) -> Dict[str, int]:
        """Calculate metrics from queryset."""
        return {
            'total': queryset.count(),
            'completed': queryset.filter(status='completed').count(),
            'in_progress': queryset.filter(status='in progress').count()
        }

def process_data(data: DataPoint) -> None:
    """Process a single data point."""
    # Validate required keys
    required_keys = {'name', 'value', 'status'}
    if not all(key in data for key in required_keys):
        raise KeyError(f"Missing required keys. Expected: {required_keys}")