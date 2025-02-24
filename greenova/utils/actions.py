from typing import Any, Dict, TypedDict, List, Callable
from functools import wraps
from time import time
from datetime import datetime
import logging
from django.db.models import QuerySet
from obligations.models import Obligation

logger = logging.getLogger(__name__)

class DataPoint(TypedDict):
    name: str
    value: int
    status: str

def log_action(action_name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator to log method execution time and status."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time()
            try:
                result = func(*args, **kwargs)
                logger.info(
                    f"{action_name} completed in {time() - start_time:.2f}s"
                )
                return result
            except Exception as e:
                logger.error(
                    f"{action_name} failed after {time() - start_time:.2f}s: {e}"
                )
                raise
        return wrapper
    return decorator

class AnalyticsActions:
    """Handle analytics-related actions."""

    @staticmethod
    @log_action("Export analytics data")
    def export_data(data: List[DataPoint]) -> Dict[str, Any]:
        """Export analytics data to structured format."""
        try:
            processed_data: List[Dict[str, Any]] = []
            for point in data:
                processed_data.append({
                    'name': point['name'],
                    'value': point['value'],
                    'status': point['status']
                })
            return {'data': processed_data, 'success': True}
        except Exception as e:
            logger.error(f"Data export failed: {e}")
            return {'error': str(e), 'success': False}

    @staticmethod
    @log_action("Generate performance report")
    def generate_report(obligations: QuerySet[Obligation]) -> Dict[str, Any]:
        """Generate performance metrics report."""
        try:
            metrics = {
                'total': obligations.count(),
                'completed': obligations.filter(status='completed').count(),
                'overdue': obligations.filter(
                    status='not started',
                    due_date__lt=datetime.now().date()
                ).count()
            }
            return {'metrics': metrics, 'success': True}
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return {'error': str(e), 'success': False}
