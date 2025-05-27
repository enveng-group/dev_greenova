"""
models.py for the reports app in Greenova.

Stub for future extensibility.
"""

from typing import ClassVar

from django.db import models


class Report(models.Model):
    """Stub model for reports."""

    name: models.CharField = models.CharField(max_length=255)
    description: models.TextField = models.TextField(blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the Report model."""
        ordering: ClassVar[list[str]] = ["-created_at"]
        verbose_name = "Report"
        verbose_name_plural = "Reports"

    def __str__(self) -> str:
        """Return the string representation of the report (its name)."""
        return self.name
