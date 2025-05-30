"""Copyright (C) 2025 Adrian Gallo.

This file is part of Greenova.

Greenova is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Greenova is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Greenova. If not, see <https://www.gnu.org/licenses/>.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

"""Models for the procedures app.

Defines the Procedure model for tracking environmental procedures and workflows.
"""
# Standard library imports
from django.db import models
from beartype import beartype
import logging
from typing import ClassVar


# Third-party imports

logger = logging.getLogger(__name__)


class Procedure(models.Model):
    """Model representing environmental procedures and workflows."""

    document_id: models.CharField = models.CharField(
        max_length=64,
        unique=True,
        help_text="Unique identifier for the procedure document.",
    )
    name: models.CharField = models.CharField(
        max_length=255,
        help_text="Name of the procedure.",
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
