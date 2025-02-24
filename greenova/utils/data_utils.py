from typing import List, TypedDict, Union, Dict, Any, Optional
from datetime import date
from django.db.models import QuerySet
import logging

logger = logging.getLogger(__name__)

class ChartDataPointType(TypedDict):
    """Type definition for a chart data point.

    Attributes:
        x: The x-axis value (typically date/time or category)
        y: The y-axis value (numeric data)
        label: Optional label for the data point
    """
    x: Union[str, float, int]  # x-axis value
    y: Union[float, int]       # y-axis value
    label: str                 # optional label

class ChartDataPoint(TypedDict):
    label: str
    value: int
    color: str

class TimeSeriesPoint(TypedDict):
    date: date
    count: int
    status: str

class BaseAnalyticsProcessor:
    """Generic base class for analytics processing."""

    def __init__(self, queryset: QuerySet, filter_id: Optional[int] = None) -> None:
        self.queryset = queryset
        self._apply_filter(filter_id)
        self.colors = {
            'not started': '#6c757d',
            'in progress': '#007bff',
            'completed': '#28a745',
            'overdue': '#dc3545',
            'default': '#6c757d'
        }

    def _apply_filter(self, filter_id: Optional[int]) -> None:
        """Apply initial filtering to queryset."""
        if filter_id:
            self.queryset = self.queryset.filter(id=filter_id)

    def get_data(self, category: str = "all") -> Dict[str, List[ChartDataPoint]]:
        """Generic method to get data - override in subclasses."""
        raise NotImplementedError("Subclasses must implement get_data")

    def get_color(self, key: str) -> str:
        """Get color for a given key."""
        return self.colors.get(key.lower(), self.colors['default'])

    @staticmethod
    def format_data(data: List[ChartDataPoint]) -> Dict[str, Any]:
        """Generic method to format data for charts."""
        return {
            'labels': [item['label'] for item in data],
            'values': [item['value'] for item in data],
            'colors': [item['color'] for item in data]
        }

    def get_chart_data(self, category: str = "all") -> Dict[str, Any]:
        """Generic method to get formatted chart data."""
        try:
            data = self.get_data(category)
            return self.format_data(data["data"])
        except Exception as e:
            logger.error(f"Error generating chart data: {str(e)}")
            raise ChartDataError("Failed to generate chart data")

class ChartDataError(Exception):
    """Custom exception for chart data generation errors."""
    pass

# Add this class after BaseAnalyticsProcessor
class AnalyticsDataProcessor(BaseAnalyticsProcessor):
    """Analytics data processor implementation."""

    def get_data(self, category: str = "all") -> Dict[str, List[ChartDataPoint]]:
        """Get formatted data for charts."""
        try:
            data: List[ChartDataPoint] = []

            # Get data based on category
            if category == "all":
                queryset = self.queryset
            else:
                queryset = self.queryset.filter(category=category)

            # Process queryset data
            for item in queryset:
                data.append({
                    'label': str(item),
                    'value': 1,  # Default value, adjust based on your needs
                    'color': self.get_color(getattr(item, 'status', 'default'))
                })

            return {'data': data}

        except Exception as e:
            logger.error(f"Error processing analytics data: {str(e)}")
            return {'data': []}

def get_chart_data() -> List[ChartDataPointType]:
    data: List[ChartDataPointType] = [
        {"x": "2024-01", "y": 100, "label": "January"},
        {"x": "2024-02", "y": 150, "label": "February"}
    ]
    return data
