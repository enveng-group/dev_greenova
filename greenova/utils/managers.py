from django.db import models
from django.db.models import Count, Q, QuerySet
from datetime import datetime, timedelta
from typing import Dict, Any, List
from obligations.models import Obligation  # Update import path

class AnalyticsManager(models.Manager[Obligation]):
    def get_queryset(self) -> QuerySet[Obligation]:
        return super().get_queryset()
    """Custom manager for analytics-related queries."""

    def get_completion_metrics(self) -> Dict[str, Any]:
        """Calculate completion metrics."""
        return self.get_queryset().aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            in_progress=Count('id', filter=Q(status='in progress')),
            not_started=Count('id', filter=Q(status='not started'))
        )
    def get_mechanism_stats(self) -> List[Dict[str, Any]]:
        """Get statistics grouped by mechanism."""
        queryset = self.get_queryset()
        stats = queryset.values('primary_environmental_mechanism').annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            completion_rate=Count(
                'id',
                filter=Q(status='completed')
            ) * 100.0 / Count('id')
        )
        return list(stats)

    def get_upcoming_due(self) -> QuerySet[Obligation]:
        """Get obligations due in the next 14 days."""
        today = datetime.now().date()
        future = today + timedelta(days=14)
        return self.get_queryset().filter(
            action_due_date__range=(today, future),
            status__in=['not started', 'in progress']
        ).order_by('action_due_date')