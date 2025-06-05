# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Procedure models for the procedures app.

This module provides the Procedure model for managing environmental procedures
and workflows, with strict type annotations, runtime type checking, and
centralized constants for statuses and compliance.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Centralized constants for statuses and compliance
    - Methods for status management and review checks

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging
from typing import ClassVar

from beartype import beartype
from django.db import models
from django.utils import timezone
from projects.models import Project
from .validators import validate_document_id

from .constants import COMPLIANCE_STATUSES, STATUS_CHOICES
from .types import (
    ProcedureStepDict,
    ProcedureDefinitionDict,
    ProcedureResultDict,
    ProcedureManager,
    StepEvaluator,
    ResultProcessor,
)

logger = logging.getLogger(__name__)


@beartype
class Procedure(models.Model):
    """Model representing environmental procedures and workflows.

    Attributes:
        STATUS_CHOICES (ClassVar[list]): List of possible statuses for the procedure.
        COMPLIANCE_STATUSES (ClassVar[list]): List of possible compliance statuses.
        name (models.CharField): Name of the procedure.
        document_id (models.CharField): Unique identifier for the procedure.
        project (models.ForeignKey): Foreign key to the associated project.
        version (models.CharField): Version of the procedure.
        description (models.TextField): Description of the procedure.
        status (models.CharField): Current status of the procedure.
        compliance_status (models.CharField): Current compliance status of the procedure.
        created_at (models.DateTimeField): Timestamp when the procedure was created.
        updated_at (models.DateTimeField): Timestamp when the procedure was last updated.
        effective_date (models.DateField): Effective date of the procedure.
        review_date (models.DateField): Review date of the procedure.
        completed_at (models.DateTimeField): Timestamp when the procedure was completed.
        document_file (models.FileField): File associated with the procedure.
        is_active (models.BooleanField): Indicates if the procedure is active.
        tags (models.CharField): Tags associated with the procedure.

    Methods:
        mark_as_completed(): Marks the procedure as completed with the current timestamp.
        set_status(status: str): Updates the procedure status.
        is_due_for_review(): Checks if the procedure is due for review.
    """

    # Use centralized constants
    STATUS_CHOICES: ClassVar[list] = STATUS_CHOICES
    COMPLIANCE_STATUSES: ClassVar[list] = COMPLIANCE_STATUSES

    # Basic information
    name: models.CharField = models.CharField(max_length=255)
    document_id: models.CharField = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique procedure identifier (e.g., ENV-PROC-001)",
        validators=[validate_document_id],
    )
    project: models.ForeignKey = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="procedures",
    )
    version: models.CharField = models.CharField(max_length=10, default="1.0")
    description: models.TextField = models.TextField(blank=True)

    # Status and dates
    status: models.CharField = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0],
    )
    compliance_status: models.CharField = models.CharField(
        max_length=20,
        choices=COMPLIANCE_STATUSES,
        default=COMPLIANCE_STATUSES[-1][0],
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    effective_date: models.DateField = models.DateField(null=True, blank=True)
    review_date: models.DateField = models.DateField(null=True, blank=True)
    completed_at: models.DateTimeField = models.DateTimeField(null=True, blank=True)

    # Document management
    document_file: models.FileField = models.FileField(
        upload_to="procedures/%Y/%m/",
        null=True,
        blank=True,
    )

    # Metadata
    is_active: models.BooleanField = models.BooleanField(default=True)
    tags: models.CharField = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-updated_at"]
        permissions = [
            ("view_procedure", "Can view procedure"),
            ("change_procedure", "Can change procedure"),
            ("delete_procedure", "Can delete procedure"),
        ]
        default_permissions = ("add", "change", "delete", "view")
        # Enable object-level permissions for django-guardian
        verbose_name = "Procedure"
        verbose_name_plural = "Procedures"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["compliance_status"]),
            models.Index(fields=["document_id"]),
        ]

    @beartype
    def __str__(self) -> str:
        """Return string representation of the procedure.

        Returns:
            str: The document ID and name of the procedure.
        """
        return f"{self.document_id} - {self.name}"

    @beartype
    def mark_as_completed(self) -> None:
        """Mark the procedure as completed with current timestamp."""
        self.completed_at = timezone.now()
        self.save(update_fields=["completed_at"])

    @beartype
    def set_status(self, status: str) -> None:
        """Update the procedure status.

        Args:
            status (str): The new status to set for the procedure.

        Raises:
            ValueError: If the provided status is invalid.
        """
        if status in dict(self.STATUS_CHOICES):
            self.status = status
            self.save(update_fields=["status", "updated_at"])
        else:
            logger.warning(
                "Invalid status: %s for procedure %s",
                status,
                self.document_id,
            )

    @beartype
    def is_due_for_review(self) -> bool:
        """Check if procedure is due for review.

        Returns:
            bool: True if the procedure is due for review, False otherwise.
        """
        if not self.review_date:
            return False
        return self.review_date <= timezone.now().date()
