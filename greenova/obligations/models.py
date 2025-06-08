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
from typing import Any

from beartype import beartype
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from guardian.models import UserObjectPermission
from projects.models import Project
from slugify import slugify

try:
    from responsibility.models import ResponsibilityAssignment
except ImportError:
    ResponsibilityAssignment = None  # type: ignore

try:
    from pb_model.models import ProtoBufMixin
except ImportError:

    class ProtoBufMixin:
        pass


try:
    from .obligations_pb2 import ObligationProto
except ImportError:
    ObligationProto = None

from core.constants import (
    FREQUENCY_ANNUALLY,
    FREQUENCY_DAILY,
    FREQUENCY_MONTHLY,
    FREQUENCY_QUARTERLY,
    FREQUENCY_WEEKLY,
    OBLIGATION_STATUS_CHOICES,
    STATUS_NOT_STARTED,
)
from core.frequency import normalize_frequency
from obligations.validators import validate_obligation_number

logger: logging.Logger = logging.getLogger(__name__)


def get_normalize_frequency():
    return normalize_frequency


class Obligation(ProtoBufMixin, models.Model):
    """Represents an environmental obligation."""

    pb_model = ObligationProto

    obligation_number = models.CharField(
        max_length=20,
        primary_key=True,
        help_text="Format: PCEMP-XXX where XXX is a number",
        validators=[validate_obligation_number],
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="obligations",
    )
    primary_environmental_mechanism = models.ForeignKey(
        "mechanisms.EnvironmentalMechanism",
        on_delete=models.PROTECT,
        related_name="obligations",
        null=True,
        verbose_name="Environmental Mechanism",
    )
    procedure = models.TextField(
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
    environmental_aspect = models.CharField(
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
    custom_environmental_aspect = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=(
            "If 'Other' is selected for Environmental Aspect, please specify "
            "the custom aspect here"
        ),
    )
    obligation = models.TextField()
    accountability = models.CharField(
        max_length=255,
        choices=[
            ("Perdaman", "Perdaman"),
            ("SCJV", "SCJV"),
            ("SCJV-during construction", "SCJV-during construction"),
            ("Perdaman-during operations", "Perdaman-during operations"),
        ],
    )
    responsible_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="responsibility.ResponsibilityAssignment",
        related_name="obligations_with_responsibility",
        blank=True,
        help_text="Users assigned to this obligation with a responsibility role.",
    )
    project_phase = models.CharField(
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
    action_due_date = models.DateField(null=True)
    close_out_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=OBLIGATION_STATUS_CHOICES,
        default=STATUS_NOT_STARTED,
    )
    supporting_information = models.TextField(blank=True, null=True)
    general_comments = models.TextField(blank=True, null=True)
    evidence_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Notes about the uploaded evidence",
    )
    recurring_obligation = models.BooleanField(default=False)
    recurring_frequency = models.CharField(
        max_length=50,
        null=True,
        choices=[
            ("Daily", "Daily"),
            ("Weekly", "Weekly"),
            ("Fortnightly", "Fortnightly"),
            ("Monthly", "Monthly"),
            ("Quarterly", "Quarterly"),
            ("Annually", "Annually"),
            ("As Required", "As Required"),
            ("Mobilisation", "Mobilisation"),
            ("Decommissioning", "Decommissioning"),
            ("Extreme Weather", "Extreme Weather"),
        ],
    )
    recurring_status = models.CharField(
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
    recurring_forecasted_date = models.DateField(
        blank=True,
        null=True,
    )
    inspection = models.BooleanField(default=False)
    inspection_frequency = models.CharField(
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
    site_or_desktop = models.CharField(
        max_length=10,
        choices=[("Site", "Site"), ("Desktop", "Desktop")],
        null=True,
    )
    new_control_action_required = models.BooleanField(
        default=False,
    )
    obligation_type = models.CharField(
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
    gap_analysis = models.BooleanField(default=False)
    notes_for_gap_analysis = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Obligation"
        verbose_name_plural = "Obligations"
        ordering = ["obligation_number"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["action_due_date"]),
            models.Index(fields=["project"]),
        ]
        # Removed explicit view/change/delete permissions to avoid clash with builtins
        default_permissions = ("add", "change", "delete", "view")

    objects = models.Manager()  # Default manager
    guardian = UserObjectPermission.objects

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
        normalize_frequency = get_normalize_frequency()

        if not self.recurring_obligation or not self.recurring_frequency:
            return None

        base_date = (
            self.recurring_forecasted_date
            or self.action_due_date
            or timezone.now().date()
        )
        today = timezone.now().date()
        base_date = max(base_date, today)
        normalized_frequency = normalize_frequency(self.recurring_frequency)

        if normalized_frequency == FREQUENCY_DAILY:
            return base_date + relativedelta(days=1)
        if normalized_frequency == FREQUENCY_WEEKLY:
            return base_date + relativedelta(weeks=1)
        if normalized_frequency == "fortnightly":
            return base_date + relativedelta(weeks=2)
        # TODO: Add FREQUENCY_FORTNIGHTLY to core/constants.py for consistency
        if normalized_frequency == FREQUENCY_MONTHLY:
            return base_date + relativedelta(months=1)
        if normalized_frequency == FREQUENCY_QUARTERLY:
            return base_date + relativedelta(months=3)
        if normalized_frequency == FREQUENCY_ANNUALLY:
            return base_date + relativedelta(years=1)
        # if normalized_frequency == FREQUENCY_BIANNUAL:
        #     return base_date + relativedelta(months=6)
        # TODO: Add support for biannual frequency if needed
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

        next_date = self.calculate_next_recurring_date()
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
        prefix = "PCEMP-"
        highest_number = 0
        all_obligations = cls.objects.all().iterator()

        for obligation in all_obligations:
            if obligation.obligation_number and obligation.obligation_number.startswith(
                prefix,
            ):
                try:
                    number_part = obligation.obligation_number[len(prefix):]
                    current_number = int(number_part)
                    highest_number = max(highest_number, current_number)
                except (ValueError, IndexError):
                    continue

        next_number = highest_number + 1
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

        if not self.slug:
            self.slug = slugify(f"{self.project}-{self.obligation_number}")

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

    @beartype
    def to_pb(self) -> Any:
        """Serialize this Obligation instance to a Protobuf message."""
        if ObligationProto is None:
            msg = "obligations_pb2.ObligationProto is not available."
            raise RuntimeError(msg)
        proto = ObligationProto()
        proto.obligation_number = self.obligation_number or ""
        proto.project_id = str(self.project_id) if self.project_id else ""
        proto.primary_environmental_mechanism_id = (
            str(self.primary_environmental_mechanism_id)
            if self.primary_environmental_mechanism_id
            else ""
        )
        proto.procedure = self.procedure or ""
        proto.environmental_aspect = self.environmental_aspect or ""
        proto.custom_environmental_aspect = self.custom_environmental_aspect or ""
        proto.obligation = self.obligation or ""
        proto.accountability = self.accountability or ""
        proto.responsible_user_ids.extend(
            [str(user.pk) for user in self.responsible_users.all()],
        )
        proto.project_phase = self.project_phase or ""
        proto.action_due_date = (
            self.action_due_date.isoformat() if self.action_due_date else ""
        )
        proto.close_out_date = (
            self.close_out_date.isoformat() if self.close_out_date else ""
        )
        proto.status = self.status or ""
        proto.supporting_information = self.supporting_information or ""
        proto.general_comments = self.general_comments or ""
        proto.evidence_notes = self.evidence_notes or ""
        proto.recurring_obligation = bool(self.recurring_obligation)
        proto.recurring_frequency = self.recurring_frequency or ""
        proto.recurring_status = self.recurring_status or ""
        proto.recurring_forecasted_date = (
            self.recurring_forecasted_date.isoformat()
            if self.recurring_forecasted_date
            else ""
        )
        proto.inspection = bool(self.inspection)
        proto.inspection_frequency = self.inspection_frequency or ""
        proto.site_or_desktop = self.site_or_desktop or ""
        proto.new_control_action_required = bool(self.new_control_action_required)
        proto.obligation_type = self.obligation_type or ""
        proto.gap_analysis = bool(self.gap_analysis)
        proto.notes_for_gap_analysis = self.notes_for_gap_analysis or ""
        proto.created_at = self.created_at.isoformat() if self.created_at else ""
        proto.updated_at = self.updated_at.isoformat() if self.updated_at else ""
        return proto

    @classmethod
    @beartype
    def from_pb(cls, proto: Any) -> "Obligation":
        """Deserialize a Protobuf message to an Obligation instance (not saved)."""
        # Note: ForeignKey/M2M fields must be resolved by caller if needed
        return cls(
            obligation_number=getattr(proto, "obligation_number", ""),
            project_id=getattr(proto, "project_id", None),
            primary_environmental_mechanism_id=getattr(
                proto,
                "primary_environmental_mechanism_id",
                None,
            ),
            procedure=getattr(proto, "procedure", ""),
            environmental_aspect=getattr(proto, "environmental_aspect", ""),
            custom_environmental_aspect=getattr(
                proto,
                "custom_environmental_aspect",
                "",
            ),
            obligation=getattr(proto, "obligation", ""),
            accountability=getattr(proto, "accountability", ""),
            project_phase=getattr(proto, "project_phase", ""),
            action_due_date=getattr(proto, "action_due_date", None),
            close_out_date=getattr(proto, "close_out_date", None),
            status=getattr(proto, "status", ""),
            supporting_information=getattr(proto, "supporting_information", ""),
            general_comments=getattr(proto, "general_comments", ""),
            evidence_notes=getattr(proto, "evidence_notes", ""),
            recurring_obligation=getattr(proto, "recurring_obligation", False),
            recurring_frequency=getattr(proto, "recurring_frequency", ""),
            recurring_status=getattr(proto, "recurring_status", ""),
            recurring_forecasted_date=getattr(proto, "recurring_forecasted_date", None),
            inspection=getattr(proto, "inspection", False),
            inspection_frequency=getattr(proto, "inspection_frequency", ""),
            site_or_desktop=getattr(proto, "site_or_desktop", ""),
            new_control_action_required=getattr(
                proto,
                "new_control_action_required",
                False,
            ),
            obligation_type=getattr(proto, "obligation_type", ""),
            gap_analysis=getattr(proto, "gap_analysis", False),
            notes_for_gap_analysis=getattr(proto, "notes_for_gap_analysis", ""),
            created_at=getattr(proto, "created_at", None),
            updated_at=getattr(proto, "updated_at", None),
        )

    # All lifecycle logic is now handled via Django signals in signals.py


@beartype
class ObligationEvidence(models.Model):
    """Model to store multiple evidence files for an obligation."""

    obligation = models.ForeignKey(
        "Obligation",
        on_delete=models.CASCADE,
        related_name="evidences",
    )
    file = models.FileField(
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
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

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
        size = self.file.size
        if size < 1024:
            return f"{size} bytes"
        if size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        return f"{size / (1024 * 1024):.1f} MB"


class ComplianceComment(models.Model):
    """Stub model for compliance comments related to obligations."""

    obligation = models.ForeignKey(
        "Obligation",
        on_delete=models.CASCADE,
        related_name="compliance_comments",
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Compliance Comment"
        verbose_name_plural = "Compliance Comments"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"ComplianceComment({self.pk}) for {self.obligation}"  # pragma: no cover


class NonConformanceComment(models.Model):
    """Stub model for non-conformance comments related to obligations."""

    obligation = models.ForeignKey(
        "Obligation",
        on_delete=models.CASCADE,
        related_name="nonconformance_comments",
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Non-Conformance Comment"
        verbose_name_plural = "Non-Conformance Comments"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"NonConformanceComment({self.pk}) for {
            self.obligation
        }"  # pragma: no cover
