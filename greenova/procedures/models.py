"""Models for the procedures app.

Defines the Procedure model for tracking environmental procedures and workflows.
"""
import logging
from typing import ClassVar

from beartype import beartype
from django.db import models

logger = logging.getLogger(__name__)


class Procedure(models.Model):
    """Model representing environmental procedures and workflows."""
    document_id: models.CharField = models.CharField(
        max_length=64,
        unique=True,
        help_text="Unique identifier for the procedure document."
    )
    name: models.CharField = models.CharField(
        max_length=255,
        help_text="Name of the procedure."
    )

    class Meta:
        """Meta options for Procedure model."""
        ordering: ClassVar[list[str]] = ["-updated_at"]
        verbose_name: ClassVar[str] = "Procedure"
        verbose_name_plural: ClassVar[str] = "Procedures"
        indexes: ClassVar[list[models.Index]] = [
            models.Index(fields=["status"]),
            models.Index(fields=["compliance_status"]),
            models.Index(fields=["document_id"]),
        ]

    @beartype
    def __str__(self) -> str:
        """Return string representation of the procedure."""
        return f"{self.document_id} - {self.name}"
