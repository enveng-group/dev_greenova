"""
Models for the responsibility app.

Defines the Responsibility and ResponsibilityAssignment models for assigning
roles to users and obligations.
"""

from typing import ClassVar

from django.db import models


class Responsibility(models.Model):
    """
    Model representing a responsibility role that can be assigned to users.

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
