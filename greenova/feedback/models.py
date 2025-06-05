from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

try:
    from pb_model.models import ProtoBufMixin
except ImportError:
    ProtoBufMixin = models.Model  # fallback for type checking

try:
    from .proto.feedback_pb2 import BugReportProto
except ImportError:
    BugReportProto = None

from .constants import (
    FEEDBACK_STATUS_CHOICES,
)

User = get_user_model()


class BugReport(ProtoBufMixin, models.Model):
    """Model for storing user-submitted bug reports, integrated with protobuf3.

    Attributes:
        pb_model: The protobuf model associated with this class.
        SEVERITY_CHOICES: List of severity levels for bug reports.
        STATUS_CHOICES: List of status options for bug reports.
        FREQUENCY_CHOICES: List of frequency options for bug occurrence.
        title: Title of the bug report.
        description: Detailed description of the bug.
        environment: Environment details where the bug occurred.
        application_version: Version of the application where the bug occurred.
        operating_system: Operating system details.
        browser: Browser details, if applicable.
        device_type: Type of device where the bug occurred.
        steps_to_reproduce: Steps to reproduce the bug.
        expected_behavior: Expected result of the application.
        actual_behavior: Actual result of the application.
        error_messages: Error messages encountered, if any.
        trace_report: Trace report details, if any.
        frequency: Frequency of the bug occurrence.
        impact_severity: Severity of the bug's impact.
        user_impact: Description of the user impact due to the bug.
        workarounds: Workarounds for the bug, if any.
        additional_comments: Additional comments about the bug.
        created_by: User who created the bug report.
        created_at: Timestamp when the bug report was created.
        updated_at: Timestamp when the bug report was last updated.
        github_issue_url: URL of the related GitHub issue, if any.
        severity: Severity level of the bug.
        status: Current status of the bug report.
        admin_comment: Comments from the admin regarding the bug report.

    """

    pb_model = BugReportProto

    SEVERITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    STATUS_CHOICES = FEEDBACK_STATUS_CHOICES

    FREQUENCY_CHOICES = [
        ("always", "Always (100% of attempts)"),
        ("frequently", "Frequently (about 7 out of 10 attempts)"),
        ("occasionally", "Occasionally (about 3 out of 10 attempts)"),
        ("rarely", "Rarely (happened once or twice)"),
    ]

    # Summary section
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))

    # Environment section
    environment = models.TextField(_("Environment Details"))
    application_version = models.CharField(_("Application Version"), max_length=50)
    operating_system = models.CharField(_("Operating System"), max_length=100)
    browser = models.CharField(_("Browser (if applicable)"), max_length=100, blank=True)
    device_type = models.CharField(_("Device Type"), max_length=100)

    # Steps section
    steps_to_reproduce = models.TextField(_("Steps to Reproduce"))
    expected_behavior = models.TextField(_("Expected Result"))
    actual_behavior = models.TextField(_("Actual Result"))

    # Technical details
    error_messages = models.TextField(_("Error Messages"), blank=True)
    trace_report = models.TextField(_("Trace Report"), blank=True)

    # Frequency and impact
    frequency = models.CharField(
        _("Frequency"),
        max_length=20,
        choices=FREQUENCY_CHOICES,
    )
    impact_severity = models.CharField(
        _("Impact Severity"),
        max_length=10,
        choices=SEVERITY_CHOICES,
        default="medium",
    )
    user_impact = models.TextField(_("User Impact Description"))

    # Additional info
    workarounds = models.TextField(_("Workarounds"), blank=True)
    additional_comments = models.TextField(_("Additional Comments"), blank=True)

    # Meta information
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="bug_reports",
        verbose_name=_("Created By"),
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    # Admin fields
    github_issue_url = models.URLField(_("GitHub Issue URL"), blank=True, null=True)
    severity = models.CharField(
        _("Severity"),
        max_length=10,
        choices=SEVERITY_CHOICES,
        default="medium",
    )
    status = models.CharField(
        _("Status"),
        max_length=15,
        choices=STATUS_CHOICES,
        default="open",
    )
    admin_comment = models.TextField(_("Admin Comment"), blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Bug Report")
        verbose_name_plural = _("Bug Reports")
        default_permissions = ("add", "change", "delete", "view")
        # Enable object-level permissions for django-guardian

    def __str__(self) -> str:
        return self.title
