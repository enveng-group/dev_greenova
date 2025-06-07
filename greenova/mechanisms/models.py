# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Models for mechanisms app.

Defines the EnvironmentalMechanism model and related database structures for
tracking environmental mechanisms and their obligations.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import logging
from typing import Any

import bleach
from core.constants import (
    STATUS_CHOICES,
    STATUS_COMPLETED,
    STATUS_IN_PROGRESS,
    STATUS_NOT_STARTED,
    STATUS_OVERDUE,
)
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.db import models

logger = logging.getLogger(__name__)


class EnvironmentalMechanism(models.Model):
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
        primary_environmental_mechanism (models.CharField): Primary environmental
            mechanism.
        created_at (models.DateTimeField): Timestamp of creation.
        updated_at (models.DateTimeField): Timestamp of last update.

    """

    name = models.CharField(max_length=255)
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="mechanisms",
    )
    description = models.TextField(blank=True, null=True)
    category = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    reference_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    effective_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NOT_STARTED,
    )

    not_started_count = models.IntegerField(default=0)
    in_progress_count = models.IntegerField(default=0)
    completed_count = models.IntegerField(default=0)
    overdue_count = models.IntegerField(default=0)

    primary_environmental_mechanism = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name: str = "Environmental Mechanism"
        verbose_name_plural: str = "Environmental Mechanisms"
        ordering: list[str] = ["name"]
        # Removed explicit view/change/delete permissions to avoid clash with builtins
        default_permissions = ("add", "change", "delete", "view")

    def __str__(self) -> str:
        """Return the string representation of the mechanism.

        Returns:
            str: The name of the mechanism.

        """
        return self.name

    @property
    def total_obligations(self) -> int:
        """Total number of obligations.

        Returns:
            int: The total number of obligations.

        """
        return self.not_started_count + self.in_progress_count + self.completed_count

    def update_obligation_counts(self) -> None:
        """Update obligation counts based on related obligations.

        Raises:
            Exception: If updating counts fails.

        """
        from obligations.models import Obligation

        obligations = Obligation.objects.filter(
            primary_environmental_mechanism=self,
        )

        self.not_started_count = 0
        self.in_progress_count = 0
        self.completed_count = 0
        self.overdue_count = 0

        for obligation in obligations:
            status = obligation.status

            if status == STATUS_OVERDUE:
                self.overdue_count += 1

            if status == STATUS_NOT_STARTED:
                self.not_started_count += 1
            elif status == STATUS_IN_PROGRESS:
                self.in_progress_count += 1
            elif status == STATUS_COMPLETED:
                self.completed_count += 1

        self.save()

    def get_status_data(self) -> dict[str, Any]:
        """Return a dictionary of status counts for charting.

        Returns:
            dict[str, Any]: Dictionary of status counts.

        """
        return {
            "Overdue": self.overdue_count,
            "Not Started": max(0, self.not_started_count - self.overdue_count),
            "In Progress": self.in_progress_count,
            "Completed": self.completed_count,
        }

    def save(self, *args: object, **kwargs: object) -> None:
        """Override save to sanitize description with bleach."""
        if self.description:
            self.description = bleach.clean(self.description)
        super().save(*args, **kwargs)


def update_all_mechanism_counts() -> int:
    """Update obligation counts for all mechanisms.

    Called after importing obligations to ensure counts are accurate.

    Returns:
        int: The number of mechanisms updated.

    """
    mechanisms = EnvironmentalMechanism.objects.all().select_related(
        "project",
    )
    updated_count = 0

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
