from typing import Dict, Any
from datetime import datetime
import logging
from django.db.models import QuerySet
from obligations.models import Obligation
from utils.actions import log_action

logger = logging.getLogger(__name__)


class ObligationAnalytics:
    """Handle obligation-specific analytics actions."""

    @staticmethod
    @log_action("Generate performance report")
    def generate_report(obligations: QuerySet[Obligation]) -> Dict[str, Any]:
        """Generate performance metrics report for obligations."""
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
