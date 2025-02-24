from django.db.models import QuerySet
from typing import Any, Optional
from obligations.models import Obligation


class ObligationFilter:
    """Filter obligations based on various criteria."""

    def __init__(self, queryset: QuerySet[Obligation]) -> None:
        self.queryset = queryset

    def filter_by_mechanism(self, mechanism: str) -> QuerySet[Obligation]:
        """Filter obligations by environmental mechanism."""
        return self.queryset.filter(primary_environmental_mechanism=mechanism)

    def filter_by_status(self, status: str) -> QuerySet[Obligation]:
        """Filter obligations by status."""
        return self.queryset.filter(status=status)

    def filter_by_aspect(self, aspect: str) -> QuerySet[Obligation]:
        """Filter obligations by environmental aspect."""
        return self.queryset.filter(environmental_aspect=aspect)

    def filter_by_date_range(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> QuerySet[Obligation]:
        """Filter obligations by due date range."""
        filters: dict[str, Any] = {}

        if start_date:
            filters['action_due_date__gte'] = start_date
        if end_date:
            filters['action_due_date__lte'] = end_date

        return self.queryset.filter(**filters)
