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

"""Data models for the feedback app in Greenova."""

# Standard library imports

# Third-party imports

from django.utils.translation import gettext_lazy as _
from django.db import models
from typing import ClassVar
from django.contrib.auth import get_user_model

User = get_user_model()


class BugReport(models.Model):
    """Model for storing user-submitted bug reports."""

    SEVERITY_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    STATUS_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
        ("rejected", "Rejected"),  # Added rejected status
    ]

    FREQUENCY_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("always", "Always (100% of attempts)"),
        ("frequently", "Frequently (about 7 out of 10 attempts)"),
        ("occasionally", "Occasionally (about 3 out of 10 attempts)"),
        ("rarely", "Rarely (happened once or twice)"),
    ]

    # Summary section
    title: models.CharField = models.CharField(_("Title"), max_length=200)
    description: models.TextField = models.TextField(_("Description"))

    # Environment section
    environment: models.TextField = models.TextField(_("Environment Details"))
    application_version: models.CharField = models.CharField(
        _("Application Version"), max_length=50,
    )
    operating_system: models.CharField = models.CharField(
        _("Operating System"), max_length=100,
    )
    browser: models.CharField = models.CharField(
        _("Browser (if applicable)"), max_length=100, blank=True,
    )
    device_type: models.CharField = models.CharField(_("Device Type"), max_length=100)

    # Steps section
    steps_to_reproduce: models.TextField = models.TextField(_("Steps to Reproduce"))
    expected_behavior: models.TextField = models.TextField(_("Expected Result"))
    actual_behavior: models.TextField = models.TextField(_("Actual Result"))

    # Technical details
    error_messages: models.TextField = models.TextField(_("Error Messages"), blank=True)
    trace_report: models.TextField = models.TextField(_("Trace Report"), blank=True)

    # Frequency and impact
    frequency: models.CharField = models.CharField(
        _("Frequency"), max_length=20, choices=FREQUENCY_CHOICES,
    )
    impact_severity: models.CharField = models.CharField(
        _("Impact Severity"), max_length=10, choices=SEVERITY_CHOICES, default="medium",
    )
    user_impact: models.TextField = models.TextField(_("User Impact Description"))

    # Additional info
    workarounds: models.TextField = models.TextField(_("Workarounds"), blank=True)
    additional_comments: models.TextField = models.TextField(
        _("Additional Comments"), blank=True,
    )

    # Meta information
    created_by: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="bug_reports",
        verbose_name=_("Created By"),
    )
    created_at: models.DateTimeField = models.DateTimeField(
        _("Created At"), auto_now_add=True,
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        _("Updated At"), auto_now=True,
    )

    # Admin fields
    github_issue_url: models.URLField = models.URLField(
        _("GitHub Issue URL"), blank=True, null=True,
    )
    severity: models.CharField = models.CharField(
        _("Severity"), max_length=10, choices=SEVERITY_CHOICES, default="medium",
    )
    status: models.CharField = models.CharField(
        _("Status"), max_length=15, choices=STATUS_CHOICES, default="open",
    )
    admin_comment: models.TextField = models.TextField(_("Admin Comment"), blank=True)

    class Meta:
        """Meta options for the BugReport model."""

        ordering: ClassVar[list[str]] = ["-created_at"]
        verbose_name = _("Bug Report")
        verbose_name_plural = _("Bug Reports")

    def __str__(self) -> str:
        """Return the string representation of the bug report (its title)."""
        return self.title
