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

"""models.py for the reports app in Greenova.

Stub for future extensibility.
"""

# Standard library imports

# Third-party imports


from beartype import beartype
from django.db import models
from typing import ClassVar


@beartype
class Report(models.Model):
    """Stub model for reports.

    Attributes:
        name (models.CharField): The name of the report.
        description (models.TextField): A brief description of the report.
        created_at (models.DateTimeField): The timestamp when the report was created.
        updated_at (models.DateTimeField): The timestamp when the report was last updated.

    """

    name: models.CharField = models.CharField(max_length=255)
    description: models.TextField = models.TextField(blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the Report model."""

        ordering: ClassVar[list[str]] = ["-created_at"]
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        # Removed explicit view/change/delete permissions to avoid clash with builtins
        default_permissions = ("add", "change", "delete", "view")
        # Enable object-level permissions for django-guardian

    def __str__(self) -> str:
        """Return the string representation of the report (its name)."""
        return self.name
