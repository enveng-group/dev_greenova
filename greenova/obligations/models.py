"""Obligation models for environmental compliance management.

Defines Django ORM models for environmental obligations and evidence,
with strict type annotations, Google style docstrings, and runtime
type checking using beartype. Integrates django-guardian for object-level
permissions and django-lifecycle for model hooks.

Author:
    Adrian Gallo <agallo@enveng-group.com.au>

License:
    AGPL-3.0
"""

import logging
import re
from datetime import date
from typing import Any, ClassVar, Iterator

from beartype import beartype
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django_lifecycle import AFTER_SAVE, BEFORE_SAVE, LifecycleModel, hook
from guardian.models import UserObjectPermission
from projects.models import Project
from responsibility.models import ResponsibilityAssignment

from .commons import OBLIGATION_STATUS_CHOICES, normalize_frequency
from .constants import (
    FREQUENCY_ANNUAL,
    FREQUENCY_BIANNUAL,
    FREQUENCY_DAILY,
    FREQUENCY_FORTNIGHTLY,
    FREQUENCY_MONTHLY,
    FREQUENCY_QUARTERLY,
    FREQUENCY_WEEKLY,
    STATUS_NOT_STARTED,
)
from .validators import validate_obligation_number
from .types import ObligationDataDict, ComplianceStatusDict, ObligationDataManager, ComplianceChecker, StatusEvaluator

try:
    from pb_model.models import ProtoBufMixin
except ImportError:
    ProtoBufMixin: type = models.Model  # type: ignore

try:
    from .proto.obligations_pb2 import ObligationProto
except ImportError:
    ObligationProto = None

logger: logging.Logger = logging.getLogger(__name__)


@beartype
class Obligation(LifecycleModel, ProtoBufMixin):
    """Represents an environmental obligation.

    Integrates django-guardian for object-level permissions. Use ProjectRole to
    assign/view permissions for users on obligations. Example usage:

        assign_perm('view_obligation', user, obligation)
        assign_perm('change_obligation', user, obligation)
        get_perms(user, obligation)

    Uses django-lifecycle for model hooks.
    """

    pb_model: ClassVar[Any] = ObligationProto

    obligation_number: models.CharField = models.CharField(
        max_length=20,
        primary_key=True,
        help_text="Format: PCEMP-XXX where XXX is a number",
        validators=[validate_obligation_number],
    )
    project: models.ForeignKey = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="obligations",
    )
    primary_environmental_mechanism: models.ForeignKey = models.ForeignKey(
        "mechanisms.EnvironmentalMechanism",
        on_delete=models.PROTECT,
        related_name="obligations",
        null=True,
        verbose_name="Environmental Mechanism",
    )
    procedure: models.TextField = models.TextField(
        default="Missing procedure",
        help_text="Procedure to follow for this obligation",
        choices=[
            ("Cultural Heritage Management", "Cultural Heritage Management"),
            ("Threated Species Management", "Threated Species Management"),
            ("Lighting Management", "Lighting Management"),
            ("Surface Water Management", "Surface Water Management"),
            ("Solid & Liquid Waste Management", "Solid & Liquid Waste Management"),
            ("Dust Management", "Dust Management"),
            ("Pest Management", "Pest Management"),
            ("Other", "Other"),
        ],
    )
    environmental_aspect: models.CharField = models.CharField(
        max_length=255,
        choices=[
            ("Air", "Air"),
            ("Water", "Water"),
            ("Waste", "Waste"),
            ("Energy", "Energy"),
            ("Biodiversity", "Biodiversity"),
            ("Noise", "Noise"),
            ("Chemicals", "Chemicals"),
            ("Soil", "Soil"),
            ("Administration", "Administration"),
            ("Cultural Heritage Management", "Cultural Heritage Management"),
            ("Terrestrial Fauna Management", "Terrestrial Fauna Management"),
            ("Biosecurity And Pest Management", "Biosecurity And Pest Management"),
            ("Dust Management", "Dust Management"),
            ("Reporting", "Reporting"),
            ("Noise Management", "Noise Management"),
            (
                "Erosion And Sedimentation Management",
                "Erosion And Sedimentation Management",
            ),
            (
                "Hazardous Substances And Hydrocarbon Management",
                "Hazardous Substances And Hydrocarbon Management",
            ),
            ("Waste Management", "Waste Management"),
            ("Artificial Light Management", "Artificial Light Management"),
            ("Audits And Inspections", "Audits And Inspections"),
            (
                "Design And Construction Requirements",
                "Design And Construction Requirements",
            ),
            ("Regulatory Compliance Reporting", "Regulatory Compliance Reporting"),
            ("Other", "Other"),
        ],
    )
    custom_environmental_aspect: models.CharField = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=(
            "If 'Other' is selected for Environmental Aspect, please specify "
            "the custom aspect here"
        ),
    )
    obligation: models.TextField = models.TextField()
    accountability: models.CharField = models.CharField(
        max_length=255,
        choices=[
            ("Perdaman", "Perdaman"),
            ("SCJV", "SCJV"),
            ("SCJV-during construction", "SCJV-during construction"),
            ("Perdaman-during operations", "Perdaman-during operations"),
        ],
    )
    responsible_users: models.ManyToManyField = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through=ResponsibilityAssignment,
        related_name="obligations_with_responsibility",
        blank=True,
        help_text="Users assigned to this obligation with a responsibility role.",
    )
    project_phase: models.CharField = models.CharField(
        max_length=255,
        null=True,
        choices=[
            ("Pre-Construction", "Pre-Construction"),
            ("Construction", "Construction"),
            ("Operation", "Operation"),
            ("Decommissioning", "Decommissioning"),
            ("Post-Closure", "Post-Closure"),
            ("Other", "Other"),
        ],
    )
    action_due_date: models.DateField = models.DateField(null=True)
    close_out_date: models.DateField = models.DateField(null=True, blank=True)
    status: models.CharField = models.CharField(
        max_length=20,
        choices=OBLIGATION_STATUS_CHOICES,
        default=STATUS_NOT_STARTED,
    )
    supporting_information: models.TextField = models.TextField(blank=True, null=True)
    general_comments: models.TextField = models.TextField(blank=True, null=True)
    evidence_notes: models.TextField = models.TextField(
        blank=True,
        null=True,
        help_text="Notes about the uploaded evidence",
    )
    recurring_obligation: models.BooleanField = models.BooleanField(default=False)
    recurring_frequency: models.CharField = models.CharField(
        max_length=50,
        null=True,
        choices=[
            ("Daily", "Daily"),
            ("Weekly", "Weekly"),
            ("Fortnightly", "Fortnightly"),
            ("Monthly", "Monthly"),
            ("Quarterly", "Quarterly"),
            ("Annually", "Annually"),
            ("Bi-Annually", "Bi-Annually"),
            ("As Required", "As Required"),
            ("Mobilisation", "Mobilisation"),
            ("Decommissioning", "Decommissioning"),
            ("Extreme Weather", "Extreme Weather"),
        ],
    )
    recurring_status: models.CharField = models.CharField(
        max_length=50,
        default="not started",
        null=True,
        choices=[
            ("not started", "Not Started"),
            ("in progress", "In Progress"),
            ("completed", "Completed"),
            ("overdue", "Overdue"),
        ],
    )
    recurring_forecasted_date: models.DateField = models.DateField(
        blank=True,
        null=True,
    )
    inspection: models.BooleanField = models.BooleanField(default=False)
    inspection_frequency: models.CharField = models.CharField(
        max_length=50,
        null=True,
        choices=[
            ("Daily", "Daily"),
            ("Weekly", "Weekly"),
            ("Fortnightly", "Fortnightly"),
            ("Monthly", "Monthly"),
            ("Quarterly", "Quarterly"),
            ("Annually", "Annually"),
        ],
    )
    site_or_desktop: models.CharField = models.CharField(
        max_length=10,
        choices=[("Site", "Site"), ("Desktop", "Desktop")],
        null=True,
    )
    new_control_action_required: models.BooleanField = models.BooleanField(default=False)
    obligation_type: models.CharField = models.CharField(
        max_length=50,
        null=True,
        choices=[
            ("Training", "Training"),
            ("Monitoring", "Monitoring"),
            ("Reporting", "Reporting"),
            ("Site based", "Site based"),
            ("Incident response", "Incident response"),
            ("Plant mobilisation", "Plant mobilisation"),
            ("Consultations", "Consultations"),
            ("Design", "Design"),
            ("Procurement", "Procurement"),
            ("Safety", "Safety"),
        ],
    )
    gap_analysis: models.BooleanField = models.BooleanField(default=False)
    notes_for_gap_analysis: models.TextField = models.TextField(blank=True, null=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Obligation"
        verbose_name_plural = "Obligations"
        ordering = ["obligation_number"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["action_due_date"]),
            models.Index(fields=["project"]),
        ]
        permissions = [
            ("view_obligation", "Can view obligation"),
            ("change_obligation", "Can change obligation"),
            ("delete_obligation", "Can delete obligation"),
        ]
        default_permissions = ("add", "change", "delete", "view")

    objects: models.Manager = models.Manager()  # Default manager
    guardian: Any = UserObjectPermission.objects

    @beartype
    def __str__(self) -> str:
        """Return string representation of the obligation.

        Returns:
            str: Human-readable string for the obligation.
        """
        return f"{self.obligation_number} - {self.project.name}"

    @beartype
    def calculate_next_recurring_date(self) -> date | None:
        """Calculate the next recurring date based on frequency and current/last date.

        Returns:
            date | None: The next forecasted date or None if not applicable.
        """
        if not self.recurring_obligation or not self.recurring_frequency:
            return None

        base_date: date = (
            self.recurring_forecasted_date
            or self.action_due_date
            or timezone.now().date()
        )
        today: date = timezone.now().date()
        base_date = max(base_date, today)
        normalized_frequency: str = normalize_frequency(self.recurring_frequency)

        if normalized_frequency == FREQUENCY_DAILY:
            return base_date + relativedelta(days=1)
        if normalized_frequency == FREQUENCY_WEEKLY:
            return base_date + relativedelta(weeks=1)
        if normalized_frequency == FREQUENCY_FORTNIGHTLY:
            return base_date + relativedelta(weeks=2)
        if normalized_frequency == FREQUENCY_MONTHLY:
            return base_date + relativedelta(months=1)
        if normalized_frequency == FREQUENCY_QUARTERLY:
            return base_date + relativedelta(months=3)
        if normalized_frequency == FREQUENCY_BIANNUAL:
            return base_date + relativedelta(months=6)
        if normalized_frequency == FREQUENCY_ANNUAL:
            return base_date + relativedelta(years=1)
        logger.warning(
            "Unrecognized frequency '%s' - defaulting to monthly",
            self.recurring_frequency,
        )
        return base_date + relativedelta(months=1)

    @beartype
    def update_recurring_forecasted_date(self) -> bool:
        """Update the recurring forecasted date based on frequency and current status.

        Returns:
            bool: True if the date was updated, False otherwise.
        """
        if not self.recurring_obligation:
            return False

        next_date: date | None = self.calculate_next_recurring_date()
        if next_date != self.recurring_forecasted_date:
            self.recurring_forecasted_date = next_date
            return True
        return False

    @classmethod
    @beartype
    def get_next_obligation_number(cls) -> str:
        """Generate the next sequential obligation number in the format PCEMP-XXX.

        Returns:
            str: The next obligation number (e.g., PCEMP-101).
        """
        prefix: str = "PCEMP-"
        highest_number: int = 0
        all_obligations: Iterator[Any] = cls.objects.all().iterator()

        for obligation in all_obligations:
            if (
                obligation.obligation_number
                and obligation.obligation_number.startswith(prefix)
            ):
                try:
                    number_part: str = obligation.obligation_number[len(prefix):]
                    current_number: int = int(number_part)
                    highest_number = max(highest_number, current_number)
                except (ValueError, IndexError):
                    continue

        next_number: int = highest_number + 1
        return f"{prefix}{next_number:03d}"

    @beartype
    def clean(self) -> None:
        """Validate the obligation number format.

        Raises:
            ValidationError: If the obligation number format is invalid.
        """
        super().clean()
        if self.obligation_number and self.obligation_number.strip():
            if not re.match(r"^PCEMP-\d+$", self.obligation_number):
                raise ValidationError(
                    {
                        "obligation_number": (
                            "Obligation number must be in the format PCEMP-XXX "
                            "where XXX is a number"
                        ),
                    },
                )

    @beartype
    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save to update mechanism counts and ensure proper obligation number format.

        Args:
            *args: Positional arguments for save.
            **kwargs: Keyword arguments for save.
        """
        if not self.obligation_number or self.obligation_number.strip() == "":
            self.obligation_number = self.get_next_obligation_number()

        if not self.obligation_number.startswith("PCEMP-"):
            self.obligation_number = (
                f"PCEMP-{self.obligation_number.split('-')[-1]}"
                if "-" in self.obligation_number
                else f"PCEMP-{self.obligation_number}"
            )

        super().save(*args, **kwargs)

        if self.primary_environmental_mechanism:
            self.primary_environmental_mechanism.update_obligation_counts()

    @property
    @beartype
    def is_overdue(self) -> bool:
        """Check if obligation is overdue.

        Returns:
            bool: True if overdue, False otherwise.
        """
        if self.status != "completed" and self.action_due_date:
            return self.action_due_date < timezone.now().date()
        return False

    @property
    @beartype
    def responsibility_assignments(self) -> models.QuerySet:
        """Return all ResponsibilityAssignment objects for this obligation.

        Returns:
            QuerySet: ResponsibilityAssignment queryset for this obligation.
        """
        return ResponsibilityAssignment.objects.filter(obligation=self)

    @hook(AFTER_SAVE)
    @beartype
    def update_forecasted_date_after_save(self) -> None:
        """Update recurring forecasted date after save if needed."""
        if self.recurring_obligation and not self.recurring_forecasted_date:
            self.update_recurring_forecasted_date()

    @hook(AFTER_SAVE)
    @beartype
    def after_save_obligation(self) -> None:
        """Log after save."""
        logger.info("Obligation %s saved (lifecycle hook)", self.obligation_number)

    @hook(AFTER_SAVE)
    @beartype
    def after_save_obligation_lifecycle(self) -> None:
        """Lifecycle hook: called after saving an obligation instance."""
        logger.info(
            "Obligation %s saved (lifecycle hook, replaces signal)",
            self.obligation_number,
        )

    @hook("after_delete")
    @beartype
    def after_delete_obligation_lifecycle(self) -> None:
        """Lifecycle hook: called after deleting an obligation instance."""
        logger.info(
            "Obligation %s deleted (lifecycle hook, replaces signal)",
            self.obligation_number,
        )

    @hook(BEFORE_SAVE)
    @beartype
    def before_save_obligation(self) -> None:
        """Ensure custom aspect is set if needed.

        Raises:
            ValidationError: If 'Other' is selected but custom aspect is missing.
        """
        if (
            self.environmental_aspect == "Other"
            and not self.custom_environmental_aspect
        ):
            msg: str = "Custom environmental aspect required if 'Other' is selected."
            raise ValidationError(msg)


@beartype
class ObligationEvidence(models.Model):
    """Model to store multiple evidence files for an obligation."""

    obligation: models.ForeignKey = models.ForeignKey(
        "Obligation",
        on_delete=models.CASCADE,
        related_name="evidences",
    )
    file: models.FileField = models.FileField(
        upload_to="evidence_files/%Y/%m/%d/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "doc",
                    "docx",
                    "xls",
                    "xlsx",
                    "png",
                    "jpg",
                    "jpeg",
                    "gif",
                    "txt",
                    "csv",
                ],
            ),
        ],
        max_length=255,
        help_text="Upload evidence documents (25MB max)",
    )
    uploaded_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    description: models.CharField = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Evidence File"
        verbose_name_plural = "Evidence Files"

    @beartype
    def __str__(self) -> str:
        """Return string representation of the evidence file.

        Returns:
            str: Human-readable string for the evidence file.
        """
        return f"Evidence for {self.obligation} - {self.file.name}"

    @beartype
    def file_size(self) -> str:
        """Return the file size in a human-readable format.

        Returns:
            str: File size as a string.
        """
        size: int = self.file.size
        if size < 1024:
            return f"{size} bytes"
        if size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        return f"{size / (1024 * 1024):.1f} MB"
