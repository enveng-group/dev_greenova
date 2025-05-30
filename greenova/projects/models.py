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

"""Models for the projects app.

Defines the Project, ProjectMembership, and ProjectObligation models for
grouping obligations and managing memberships.
"""
# Standard library imports
from django.db import models
from django.contrib.auth import get_user_model
import logging
from typing import ClassVar, TypeVar


# Third-party imports

logger = logging.getLogger(__name__)

User = get_user_model()
UserType = TypeVar("UserType", bound=models.Model)  # Type variable for User model


class Project(models.Model):
    """Project model to group obligations."""

    name = models.CharField(max_length=255, unique=True, help_text="Project name.")
    # ...existing code...

    class Meta:
        """Meta options for Project model."""

        verbose_name: ClassVar[str] = "Project"
        verbose_name_plural: ClassVar[str] = "Projects"
        ordering: ClassVar[list[str]] = ["-created_at"]

    def __str__(self) -> str:
        """Return string representation of the project."""
        return self.name
    # ...existing code...


class ProjectMembership(models.Model):
    """Through model for project memberships."""

    # ...existing code...
    class Meta:
        """Meta options for ProjectMembership model."""

        unique_together: ClassVar[list[str]] = ["user", "project"]
        ordering: ClassVar[list[str]] = ["project", "user"]
        verbose_name: ClassVar[str] = "Project Membership"
        verbose_name_plural: ClassVar[str] = "Project Memberships"
    # ...existing code...


class ProjectObligation(models.Model):
    """Through model for project obligations."""

    # ...existing code...
    class Meta:
        """Meta options for ProjectObligation model."""

        unique_together: ClassVar[list[str]] = ["project", "obligation"]
        ordering: ClassVar[list[str]] = ["project", "obligation"]
        verbose_name: ClassVar[str] = "Project Obligation"
        verbose_name_plural: ClassVar[str] = "Project Obligations"
    # ...existing code...
