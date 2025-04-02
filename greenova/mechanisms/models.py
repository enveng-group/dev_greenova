import logging
from builtins import property
from typing import List

from core.types import StatusData
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.db import models
from django.db.models.query import QuerySet
from django_matplotlib.fields import MatplotlibFigureField  # type: ignore
from obligations.constants import (STATUS_CHOICES, STATUS_COMPLETED, STATUS_IN_PROGRESS,
                                   STATUS_NOT_STARTED)
from obligations.utils import is_obligation_overdue

logger = logging.getLogger(__name__)


class EnvironmentalMechanism(models.Model):
    """Represents an environmental mechanism that governs obligations."""

    name: models.CharField = models.CharField(max_length=255)
    project: models.ForeignKey = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='mechanisms'
    )
    description: models.TextField = models.TextField(blank=True, null=True)
    category: models.CharField = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    reference_number: models.CharField = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    effective_date: models.DateField = models.DateField(null=True, blank=True)

    # Add status field
    status: models.CharField = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NOT_STARTED
    )

    # Add count fields
    not_started_count: models.IntegerField = models.IntegerField(default=0)
    in_progress_count: models.IntegerField = models.IntegerField(default=0)
    completed_count: models.IntegerField = models.IntegerField(default=0)
    # Field to track overdue obligations
    overdue_count: models.IntegerField = models.IntegerField(default=0)

    primary_environmental_mechanism: models.CharField = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    # Add matplotlib figure fields
    status_chart: MatplotlibFigureField = MatplotlibFigureField(
        figure='mechanisms.figures.get_mechanism_chart',  # Full import path
        plt_args=lambda obj: (obj.id,),  # type: ignore
        fig_width=300,
        fig_height=250,
        output_format='png',
        silent=True,
    )

    class Meta:
        verbose_name: str = 'Environmental Mechanism'
        verbose_name_plural: str = 'Environmental Mechanisms'
        ordering: List[str] = ['name']

    def __str__(self) -> str:
        return self.name

    @property
    def total_obligations(self) -> int:
        """Total number of obligations."""
        return self.not_started_count + self.in_progress_count + self.completed_count

    def update_obligation_counts(self) -> None:
        """Update obligation counts based on related obligations."""
        from obligations.models import Obligation

        # Get all related obligations
        obligations: QuerySet = Obligation.objects.filter(
            primary_environmental_mechanism=self
        )

        # Reset counts
        self.not_started_count = 0
        self.in_progress_count = 0
        self.completed_count = 0
        self.overdue_count = 0

        # Count obligations by status
        for obligation in obligations:
            status = obligation.status

            # Check if overdue using the utility function
            if is_obligation_overdue(obligation):
                self.overdue_count += 1

            # Also count by regular status
            if status == STATUS_NOT_STARTED:
                self.not_started_count += 1
            elif status == STATUS_IN_PROGRESS:
                self.in_progress_count += 1
            elif status == STATUS_COMPLETED:
                self.completed_count += 1

        self.save()

    def get_status_data(self) -> StatusData:
        """Return a dictionary of status counts for charting."""
        return StatusData({
            'Overdue': self.overdue_count,
            'Not Started': max(0, self.not_started_count - self.overdue_count),
            'In Progress': self.in_progress_count,
            'Completed': self.completed_count,
        })


def update_all_mechanism_counts() -> int:
    """
    Update obligation counts for all mechanisms.
    Called after importing obligations to ensure counts are accurate.
    """
    mechanisms: QuerySet = (EnvironmentalMechanism.objects
                            .all()
                            .select_related('project'))
    updated_count: int = 0

    for mechanism in mechanisms:
        try:
            mechanism.update_obligation_counts()
            updated_count += 1
        except (
                ObjectDoesNotExist,  # Using imported exceptions
                FieldError,
                AttributeError,
                ValueError
        ) as e:
            logger.error(
                'Error updating counts for mechanism %s: %s',
                mechanism.name, str(e)
            )

    return updated_count
