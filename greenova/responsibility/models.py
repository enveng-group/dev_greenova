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

"""Models for the responsibility app.

Defines the Responsibility and ResponsibilityAssignment models for assigning
roles to users and obligations.
"""


from typing import ClassVar
from django.db import models


class Responsibility(models.Model):
    """Model representing a responsibility role that can be assigned to users.

    for specific obligations.
    """

    class Meta:
        """Meta options for Responsibility model."""

        verbose_name: ClassVar[str] = "Responsibility"
        verbose_name_plural: ClassVar[str] = "Responsibilities"
        unique_together: ClassVar[list[str]] = ["name", "company"]


class ResponsibilityAssignment(models.Model):
    """Model representing an assignment of a responsibility to a user."""

    class Meta:
        """Meta options for ResponsibilityAssignment model."""

        verbose_name: ClassVar[str] = "Responsibility Assignment"
        verbose_name_plural: ClassVar[str] = "Responsibility Assignments"
        ordering: ClassVar[list[str]] = ["-created_at"]
        unique_together: ClassVar[list[str]] = ["user", "obligation", "role"]
