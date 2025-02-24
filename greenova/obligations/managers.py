from django.db import models
from django.db.models import Count, Q, QuerySet
from datetime import datetime, timedelta
from typing import Dict, Any, List
from .utils import ObligationAnalyticsProcessor
from .models import Obligation
import logging

logger = logging.getLogger(__name__)

class AnalyticsManager(models.Manager[Obligation]):
    """Custom manager for analytics-related queries."""

    def get_queryset(self) -> QuerySet[Obligation]:
        return super().get_queryset()

    def get_completion_metrics(self) -> Dict[str, Any]:
        """Calculate completion metrics."""
        return self.get_queryset().aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            in_progress=Count('id', filter=Q(status='in progress')),
            not_started=Count('id', filter=Q(status='not started'))
        )

    def get_mechanism_stats(self) -> List[Dict[str, Any]]:
        """Get statistics grouped by mechanism using ObligationAnalyticsProcessor."""
        processor = ObligationAnalyticsProcessor(self.get_queryset())
        return processor.get_mechanism_data()['data']

    def get_upcoming_due(self) -> QuerySet[Obligation]:
        """Get obligations due in the next 14 days."""
        today = datetime.now().date()
        future = today + timedelta(days=14)
        return self.get_queryset().filter(
            action_due_date__range=(today, future),
            status__in=['not started', 'in progress']
        ).order_by('action_due_date')
