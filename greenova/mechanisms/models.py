# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Mechanism models for the mechanisms app.

This module provides the EnvironmentalMechanism model for managing environmental
mechanisms that govern obligations, with strict type annotations, runtime type
checking, and Protocol Buffer integration.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protobuf3 integration for mechanism models
    - Methods for updating obligation counts and status data

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging
from builtins import property
from typing import TYPE_CHECKING

from beartype import beartype
from core.types import StatusData
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.db import models
from django_matplotlib.fields import MatplotlibFigureField  # type: ignore
from obligations.constants import (
    STATUS_CHOICES,
    STATUS_COMPLETED,
    STATUS_IN_PROGRESS,
    STATUS_NOT_STARTED,
)
from obligations.utils import is_obligation_overdue

from .validators import validate_reference_number

try:
    from pb_model.models import ProtoBufMixin
except ImportError:
    ProtoBufMixin = models.Model  # fallback for type checking

try:
    from .proto.mechanism_pb2 import (
        ChartData,
        ChartResponse,
        ChartSegment,
        ObligationInsight,
        ObligationInsightResponse,
    )
except ImportError:
    ObligationInsight = None
    ObligationInsightResponse = None
    ChartSegment = None
    ChartData = None
    ChartResponse = None

if TYPE_CHECKING:
    from django.db.models.query import QuerySet

logger = logging.getLogger(__name__)


class EnvironmentalMechanism(ProtoBufMixin, models.Model):
    """Represents an environmental mechanism that governs obligations.

    Attributes:
        name (models.CharField): Name of the mechanism.
        project (models.ForeignKey): Associated project.
        description (models.TextField): Description of the mechanism.
        category (models.CharField): Category of the mechanism.
        reference_number (models.CharField): Reference number for the mechanism.
        effective_date (models.DateField): Effective date of the mechanism.
        status (models.CharField): Current status of the mechanism.
        not_started_count (models.IntegerField): Count of obligations not started.
        in_progress_count (models.IntegerField): Count of obligations in progress.
        completed_count (models.IntegerField): Count of completed obligations.
        overdue_count (models.IntegerField): Count of overdue obligations.
        primary_environmental_mechanism (models.CharField): Primary environmental mechanism.
        created_at (models.DateTimeField): Timestamp of creation.
        updated_at (models.DateTimeField): Timestamp of last update.
        status_chart (MatplotlibFigureField): Chart representing status data.

    """

    name: models.CharField = models.CharField(max_length=255)
    project: models.ForeignKey = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="mechanisms",
    )
    description: models.TextField = models.TextField(blank=True, null=True)
    category: models.CharField = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    reference_number: models.CharField = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        validators=[validate_reference_number],
    )
    effective_date: models.DateField = models.DateField(null=True, blank=True)

    status: models.CharField = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NOT_STARTED,
    )

    not_started_count: models.IntegerField = models.IntegerField(default=0)
    in_progress_count: models.IntegerField = models.IntegerField(default=0)
    completed_count: models.IntegerField = models.IntegerField(default=0)
    overdue_count: models.IntegerField = models.IntegerField(default=0)

    primary_environmental_mechanism: models.CharField = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    status_chart: MatplotlibFigureField = MatplotlibFigureField(
        figure="mechanisms.figures.get_mechanism_chart",
        plt_args=lambda obj: (obj.id,),  # type: ignore
        fig_width=300,
        fig_height=250,
        output_format="png",
        silent=True,
    )

    class Meta:
        verbose_name: str = "Environmental Mechanism"
        verbose_name_plural: str = "Environmental Mechanisms"
        ordering: list[str] = ["name"]
        # Removed explicit view/change/delete permissions to avoid clash with builtins
        default_permissions = ("add", "change", "delete", "view")

    @beartype
    def __str__(self) -> str:
        """Return the string representation of the mechanism.

        Returns:
            str: The name of the mechanism.

        """
        return self.name

    @property
    @beartype
    def total_obligations(self) -> int:
        """Total number of obligations.

        Returns:
            int: The total number of obligations.

        """
        return self.not_started_count + self.in_progress_count + self.completed_count

    @beartype
    def update_obligation_counts(self) -> None:
        """Update obligation counts based on related obligations.

        Raises:
            Exception: If updating counts fails.

        """
        from obligations.models import Obligation

        obligations: QuerySet = Obligation.objects.filter(
            primary_environmental_mechanism=self,
        )

        self.not_started_count = 0
        self.in_progress_count = 0
        self.completed_count = 0
        self.overdue_count = 0

        for obligation in obligations:
            status = obligation.status

            if is_obligation_overdue(obligation):
                self.overdue_count += 1

            if status == STATUS_NOT_STARTED:
                self.not_started_count += 1
            elif status == STATUS_IN_PROGRESS:
                self.in_progress_count += 1
            elif status == STATUS_COMPLETED:
                self.completed_count += 1

        self.save()

    @beartype
    def get_status_data(self) -> StatusData:
        """Return a dictionary of status counts for charting.

        Returns:
            StatusData: Dictionary of status counts.

        """
        return StatusData(
            {
                "Overdue": self.overdue_count,
                "Not Started": max(0, self.not_started_count - self.overdue_count),
                "In Progress": self.in_progress_count,
                "Completed": self.completed_count,
            },
        )


@beartype
def update_all_mechanism_counts() -> int:
    """Update obligation counts for all mechanisms.

    Called after importing obligations to ensure counts are accurate.

    Returns:
        int: The number of mechanisms updated.

    """
    mechanisms: QuerySet = EnvironmentalMechanism.objects.all().select_related(
        "project",
    )
    updated_count: int = 0

    for mechanism in mechanisms:
        try:
            mechanism.update_obligation_counts()
            updated_count += 1
        except (
            ObjectDoesNotExist,
            FieldError,
            AttributeError,
            ValueError,
        ) as e:
            logger.exception(
                "Error updating counts for mechanism %s: %s",
                mechanism.name,
                str(e),
            )

    return updated_count
