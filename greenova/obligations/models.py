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

try:
    from pb_model.models import ProtoBufMixin
except ImportError:
    ProtoBufMixin = models.Model  # fallback for type checking

try:
    from .proto.obligations_pb2 import ObligationProto
except ImportError:
    ObligationProto = None

logger = logging.getLogger(__name__)


class Obligation(LifecycleModel, ProtoBufMixin):
    """Represents an environmental obligation.

    Integrates django-guardian for object-level permissions. Use ProjectRole to
    assign/view permissions for users on obligations. Example usage:

        assign_perm('view_obligation', user, obligation)
        assign_perm('change_obligation', user, obligation)
        get_perms(user, obligation)

    Uses django-lifecycle for model hooks.
    """

    pb_model = ObligationProto

    obligation_number = models.CharField(
        max_length=20,
        primary_key=True,
        help_text="Format: PCEMP-XXX where XXX is a number",
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
    procedure: str | None = models.TextField(
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
    environmental_aspect: str = models.CharField(
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
    custom_environmental_aspect: str | None = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="If 'Other' is selected for Environmental Aspect, please specify the custom aspect here",
    )
    obligation: str = models.TextField()
    accountability: str = models.CharField(
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
        through=ResponsibilityAssignment,
        related_name="obligations_with_responsibility",
        blank=True,
        help_text="Users assigned to this obligation with a responsibility role.",
    )
    project_phase: str | None = models.CharField(
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
    action_due_date: models.DateField | None = models.DateField(null=True)
    close_out_date: models.DateField | None = models.DateField(null=True, blank=True)
    status: str = models.CharField(
        max_length=20,
        choices=OBLIGATION_STATUS_CHOICES,
        default=STATUS_NOT_STARTED,
    )
    supporting_information: str | None = models.TextField(blank=True, null=True)
    general_comments: str | None = models.TextField(blank=True, null=True)
    evidence_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Notes about the uploaded evidence",
    )
    recurring_obligation = models.BooleanField(default=False)
    recurring_frequency: str | None = models.CharField(
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
    recurring_status: str | None = models.CharField(
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
    recurring_forecasted_date: models.DateField | None = models.DateField(
        blank=True,
        null=True,
    )
    inspection = models.BooleanField(default=False)
    inspection_frequency: str | None = models.CharField(
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
    site_or_desktop: str | None = models.CharField(
        max_length=10,
        choices=[("Site", "Site"), ("Desktop", "Desktop")],
        null=True,
    )
    new_control_action_required: bool = models.BooleanField(default=False)
    obligation_type: str | None = models.CharField(
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
    gap_analysis: bool | None = models.BooleanField(default=False)
    notes_for_gap_analysis: str | None = models.TextField(blank=True, null=True)
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

    objects = models.Manager()  # Default manager
    guardian = UserObjectPermission.objects

    @beartype
    def __str__(self) -> str:
        return f"{self.obligation_number} - {self.project.name}"

    @beartype
    def calculate_next_recurring_date(self) -> date | None:
        """Calculate the next recurring date based on frequency and current/last date.

        Returns:
            date: The next forecasted date or None if not applicable

        """
        # If not recurring or no frequency, don't calculate
        if not self.recurring_obligation or not self.recurring_frequency:
            return None

        # Start from last forecasted date, due date, or today
        base_date = (
            self.recurring_forecasted_date
            or self.action_due_date
            or timezone.now().date()
        )

        # If base date is in the past, start from today
        today = timezone.now().date()
        base_date = max(base_date, today)

        # Normalize frequency
        normalized_frequency = normalize_frequency(self.recurring_frequency)

        # Calculate next date based on frequency
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
        # Default to monthly if we don't recognize the frequency
        logger.warning(
            f"Unrecognized frequency '{
                self.recurring_frequency
            }' - defaulting to monthly",
        )
        return base_date + relativedelta(months=1)

    @beartype
    def update_recurring_forecasted_date(self) -> bool:
        """Update the recurring forecasted date based on frequency and current status.

        Returns:
            bool: True if the date was updated, False otherwise

        """
        # Skip if not recurring
        if not self.recurring_obligation:
            return False

        next_date = self.calculate_next_recurring_date()

        # Check if the date changed
        if next_date != self.recurring_forecasted_date:
            self.recurring_forecasted_date = next_date
            return True

        return False

    @classmethod
    @beartype
    def get_next_obligation_number(cls) -> str:
        """Generate the next sequential obligation number in the format PCEMP-XXX.

        Returns:
            str: The next obligation number (e.g., PCEMP-101)

        """
        prefix = "PCEMP-"

        # Extract the highest numeric value from all obligation numbers
        highest_number = 0

        # Query all obligation numbers
        all_obligations = cls.objects.all()

        for obligation in all_obligations:
            if obligation.obligation_number and obligation.obligation_number.startswith(
                prefix,
            ):
                try:
                    # Extract numeric part after the prefix
                    number_part = obligation.obligation_number[len(prefix):]
                    current_number = int(number_part)

                    # Update highest if we found a larger number
                    highest_number = max(highest_number, current_number)
                except (ValueError, IndexError):
                    # Skip if we can't parse the number
                    continue

        # Increment by 1 for the next number
        next_number = highest_number + 1

        # Format with leading zeros (e.g., PCEMP-001)
        return f"{prefix}{next_number:03d}"

    @beartype
    def clean(self) -> None:
        """Validate the obligation number format."""
        super().clean()

        # Only validate if obligation_number is already set
        # This allows new records to pass validation before the number is generated
        if self.obligation_number and self.obligation_number.strip():
            if not re.match(r"^PCEMP-\d+$", self.obligation_number):
                raise ValidationError(
                    {
                        "obligation_number": "Obligation number must be in the format PCEMP-XXX where XXX is a number",
                    },
                )

    @beartype
    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save to update mechanism counts and ensure proper obligation number format."""
        # Generate a new obligation number if one isn't provided
        if not self.obligation_number or self.obligation_number.strip() == "":
            self.obligation_number = self.get_next_obligation_number()

        # Ensure the format is correct (prefix + number)
        if not self.obligation_number.startswith("PCEMP-"):
            self.obligation_number = f"PCEMP-{
                self.obligation_number.split('-')[-1]
                if '-' in self.obligation_number
                else self.obligation_number
            }"

        super().save(*args, **kwargs)

        # Update mechanism counts
        if self.primary_environmental_mechanism:
            self.primary_environmental_mechanism.update_obligation_counts()

    @property
    @beartype
    def is_overdue(self) -> bool:
        """Check if obligation is overdue."""
        from django.utils import timezone

        if self.status != "completed" and self.action_due_date:
            return self.action_due_date < timezone.now().date()
        return False

    @property
    @beartype
    def responsibility_assignments(self):
        """Return all ResponsibilityAssignment objects for this obligation."""
        from responsibility.models import ResponsibilityAssignment

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

    @hook(BEFORE_SAVE)
    @beartype
    def before_save_obligation(self) -> None:
        """Ensure custom aspect is set if needed."""
        if (
            self.environmental_aspect == "Other"
            and not self.custom_environmental_aspect
        ):
            msg = "Custom environmental aspect required if 'Other' is selected."
            raise ValidationError(msg)


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
        return f"Evidence for {self.obligation} - {self.file.name}"

    @beartype
    def file_size(self) -> str:
        """Return the file size in a human-readable format."""
        size = self.file.size
        if size < 1024:
            return f"{size} bytes"
        if size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        return f"{size / (1024 * 1024):.1f} MB"
