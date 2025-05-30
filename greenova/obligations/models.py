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

"""Models for the obligations app.

Defines the Obligation and ObligationEvidence models for tracking
environmental obligations and evidence files.
"""

# mypy: ignore-errors

# Standard library imports
from utils import normalize_frequency  # Fix import error
from roles import get_responsibility_choices
from projects.models import Project
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from constants import FREQUENCY_DISPLAY_NAMES, STATUS_CHOICES
from typing import Any, ClassVar
from datetime import date
import logging
import re


# Local application imports

# Third-party imports

logger = logging.getLogger(__name__)


class Obligation(models.Model):
    """Represents an environmental obligation."""

    obligation_number = models.CharField(
        max_length=20,
        primary_key=True,
        help_text="Format: PCEMP-XXX where XXX is a number",
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="obligations",
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
            ("Threatened Species Management", "Threatened Species Management"),
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
            "If 'Other' is selected for Environmental Aspect, "
            "please specify the custom aspect here"
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
    responsibility = models.CharField(
        max_length=255,
        choices=get_responsibility_choices(),
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
        max_length=20, choices=STATUS_CHOICES, default="not started",
    )
    supporting_information = models.TextField(
        blank=True, null=True,
    )
    general_comments = models.TextField(
        blank=True, null=True,
    )
    compliance_comments = models.TextField(
        blank=True, null=True,
    )
    non_conformance_comments = models.TextField(
        blank=True, null=True,
    )
    evidence_notes = models.TextField(
        blank=True, null=True, help_text="Notes about the uploaded evidence",
    )
    recurring_obligation = models.BooleanField(default=False)
    recurring_frequency = models.CharField(
        max_length=50,
        null=True,
        choices=[(v, v) for v in FREQUENCY_DISPLAY_NAMES.values()] + [
            ("Bi-Annually", "Bi-Annually"),
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
        blank=True, null=True,
    )
    inspection = models.BooleanField(default=False)
    inspection_frequency = models.CharField(
        max_length=50,
        null=True,
        choices=[(v, v) for v in FREQUENCY_DISPLAY_NAMES.values()],
    )
    site_or_desktop = models.CharField(
        max_length=10, choices=[("Site", "Site"), ("Desktop", "Desktop")], null=True,
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
    notes_for_gap_analysis = models.TextField(
        blank=True, null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for Obligation model."""

        verbose_name: ClassVar[str] = "Obligation"
        verbose_name_plural: ClassVar[str] = "Obligations"
        ordering: ClassVar[list[str]] = ["obligation_number"]
        indexes: ClassVar[list[Any]] = [
            models.Index(fields=["status"]),
            models.Index(fields=["action_due_date"]),
            models.Index(fields=["project"]),
        ]
        app_label: ClassVar[str] = "obligations"

    def __str__(self) -> str:
        """String representation of Obligation."""
        return (
            f"{self.obligation_number} - "
            f"{self.project.name}"
        )

    def calculate_next_recurring_date(self) -> date | None:
        """Calculate the next recurring date based on frequency and current/last date.

        Returns:
            date: The next forecasted date or None if not applicable

        """
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
        result = None
        if normalized_frequency == "daily":
            result = base_date + relativedelta(days=1)
        elif normalized_frequency == "weekly":
            result = base_date + relativedelta(weeks=1)
        elif normalized_frequency == "fortnightly":
            result = base_date + relativedelta(weeks=2)
        elif normalized_frequency == "monthly":
            result = base_date + relativedelta(months=1)
        elif normalized_frequency == "quarterly":
            result = base_date + relativedelta(months=3)
        elif normalized_frequency == "biannual":
            result = base_date + relativedelta(months=6)
        elif normalized_frequency == "annual":
            result = base_date + relativedelta(years=1)
        else:
            logger.warning(
                "Unrecognized frequency '%s' - defaulting to monthly",
                self.recurring_frequency,
            )
            result = base_date + relativedelta(months=1)
        return result

    def update_recurring_forecasted_date(self) -> bool:
        """Update the recurring forecasted date based on frequency and current status.

        Returns:
            bool: True if the date was updated, False otherwise

        """
        if not self.recurring_obligation:
            return False
        next_date = self.calculate_next_recurring_date()
        if next_date is not None and next_date != self.recurring_forecasted_date:
            self.recurring_forecasted_date = next_date
            return True
        return False

    @classmethod
    def get_next_obligation_number(cls) -> str:
        """Generate the next sequential obligation number in the format PCEMP-XXX.

        Returns:
            str: The next obligation number (e.g., PCEMP-101)

        """
        prefix = "PCEMP-"
        highest_number = 0
        all_obligations = cls.objects.all()
        for obligation in all_obligations:
            if (
                obligation.obligation_number
                and obligation.obligation_number.startswith(prefix)
            ):
                number_part = obligation.obligation_number[len(prefix):]
                try:
                    current_number = int(number_part)
                    highest_number = max(current_number, highest_number)
                except ValueError:
                    continue
        next_number = highest_number + 1
        return f"{prefix}{next_number:03d}"

    def clean(self) -> None:
        """Validate the obligation number format."""
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

    def save(self, *args: tuple, **kwargs: dict) -> None:
        """Override save to update mechanism counts and ensure proper format.

        Generates a new obligation number if one isn't provided and ensures the
        format is correct. Also updates mechanism counts after saving.
        """
        if not self.obligation_number or self.obligation_number.strip() == "":
            self.obligation_number = self.get_next_obligation_number()
        if not self.obligation_number.startswith("PCEMP-"):
            num_part = (
                self.obligation_number.split("-")[-1]
                if "-" in self.obligation_number
                else self.obligation_number
            )
            self.obligation_number = f"PCEMP-{num_part}"
        try:
            super().save(*args, **kwargs)
        except Exception as exc:
            logger.exception("Error saving obligation: %s", str(exc))
        if self.primary_environmental_mechanism:
            self.primary_environmental_mechanism.update_obligation_counts()

    @property
    def is_overdue(self) -> bool:
        """Check if obligation is overdue."""
        if self.status != "completed" and self.action_due_date:
            return self.action_due_date < timezone.now().date()
        return False


# Signal handlers to update mechanism counts
@receiver(post_save, sender=Obligation)
def update_mechanism_counts_on_save(
        sender: object,
        instance: object,
        **kwargs: dict) -> None:
    """Update mechanism counts when an obligation is saved."""
    try:
        if instance.primary_environmental_mechanism:
            instance.primary_environmental_mechanism.update_obligation_counts()
            logger.info(
                "Updated counts for mechanism %s",
                instance.primary_environmental_mechanism.name,
            )
    except Exception as e:
        logger.exception("Error updating mechanism counts on save: %s", str(e))


@receiver(post_delete, sender=Obligation)
def update_mechanism_counts_on_delete(
    sender: object, instance: object, **kwargs: dict,
) -> None:
    """Update mechanism counts when an obligation is deleted."""
    if instance.primary_environmental_mechanism:
        instance.primary_environmental_mechanism.update_obligation_counts()


class ObligationEvidence(models.Model):
    """Model to store multiple evidence files for an obligation."""

    obligation: models.ForeignKey["Obligation"] = models.ForeignKey(
        "Obligation", on_delete=models.CASCADE, related_name="evidences",
    )
    file: Any = models.FileField(
        upload_to="evidence_files/%Y/%m/%d/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf", "doc", "docx", "xls", "xlsx", "png",
                    "jpg", "jpeg", "gif", "txt", "csv",
                ],
            ),
        ],
        max_length=255,
        help_text="Upload evidence documents (25MB max)",
    )
    uploaded_at: Any = models.DateTimeField(auto_now_add=True)
    description: Any = models.CharField(max_length=255, blank=True)

    class Meta:
        """Meta options for ObligationEvidence model."""

        ordering: ClassVar[list[str]] = ["-uploaded_at"]
        verbose_name: ClassVar[str] = "Evidence File"
        verbose_name_plural: ClassVar[str] = "Evidence Files"

    def __str__(self) -> str:
        """String representation of ObligationEvidence."""
        return f"Evidence for {self.obligation} - {self.file.name}"

    def file_size(self) -> str:
        """Return the file size in a human-readable format."""
        kb: int = 1024
        mb: int = 1024 * 1024
        size = self.file.size
        if size < kb:
            return f"{size} bytes"
        if size < mb:
            return f"{size / kb:.1f} KB"
        return f"{size / mb:.1f} MB"


@receiver(pre_save, sender="obligations.Obligation")
def update_forecasted_date_on_change(
    sender: object, instance: object, **kwargs: dict,
) -> None:
    """Signal handler to update forecasted date when relevant fields change."""
    if not instance.pk:
        instance.update_recurring_forecasted_date()
        return
    try:
        old_instance = sender.objects.get(pk=instance.pk)
        if (
            instance.recurring_obligation != old_instance.recurring_obligation
            or instance.recurring_frequency != old_instance.recurring_frequency
            or instance.status != old_instance.status
            or instance.action_due_date != old_instance.action_due_date
        ):
            instance.update_recurring_forecasted_date()
        if (
            instance.status == "completed"
            and old_instance.status != "completed"
            and instance.recurring_obligation
        ):
            instance.status = "not started"
            instance.update_recurring_forecasted_date()
    except sender.DoesNotExist:
        pass


@receiver(pre_save, sender="obligations.Obligation")
def ensure_obligation_number(
    sender: object, instance: object, **kwargs: dict,
) -> None:
    """Ensure obligation has a valid number before saving.

    If it's a new record without a number, generate one.
    """
    if not instance.pk and (
        not instance.obligation_number or instance.obligation_number.strip() == ""
    ):
        instance.obligation_number = Obligation.get_next_obligation_number()
