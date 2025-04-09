import logging
import re
from datetime import date, timedelta
from typing import Any, ClassVar, Optional, Type

from core.utils.roles import get_responsibility_choices
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from projects.models import Project

from .constants import (FREQUENCY_ANNUAL, FREQUENCY_BIANNUAL, FREQUENCY_DAILY,
                        FREQUENCY_FORTNIGHTLY, FREQUENCY_MONTHLY, FREQUENCY_QUARTERLY,
                        FREQUENCY_WEEKLY, STATUS_CHOICES, STATUS_COMPLETED,
                        STATUS_IN_PROGRESS, STATUS_NOT_STARTED)
from .utils import normalize_frequency

logger = logging.getLogger(__name__)

class Obligation(models.Model):
    """Represents an environmental obligation."""
    obligation_number = models.CharField(
        max_length=20,
        primary_key=True,
        help_text='Format: PCEMP-XXX where XXX is a number'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='obligations'
    )
    primary_environmental_mechanism = models.ForeignKey(
        'mechanisms.EnvironmentalMechanism',
        on_delete=models.PROTECT,
        related_name='obligations',
        null=True,
        verbose_name='Environmental Mechanism'
    )
    procedure: Optional[str] = models.TextField(
        default='Missing procedure',
        help_text='Procedure to follow for this obligation',
        choices=[
            ('Cultural Heritage Management', 'Cultural Heritage Management'),
            ('Threated Species Management', 'Threated Species Management'),
            ('Lighting Management', 'Lighting Management'),
            ('Surface Water Management', 'Surface Water Management'),
            ('Solid & Liquid Waste Management', 'Solid & Liquid Waste Management'),
            ('Dust Management', 'Dust Management'),
            ('Pest Management', 'Pest Management'),
            ('Other', 'Other'),
        ]
    )
    environmental_aspect: str = models.CharField(
        max_length=255,
        choices=[
            ('Air', 'Air'),
            ('Water', 'Water'),
            ('Waste', 'Waste'),
            ('Energy', 'Energy'),
            ('Biodiversity', 'Biodiversity'),
            ('Noise', 'Noise'),
            ('Chemicals', 'Chemicals'),
            ('Soil', 'Soil'),
            ('Administration', 'Administration'),
            ('Cultural Heritage Management', 'Cultural Heritage Management'),
            ('Terrestrial Fauna Management', 'Terrestrial Fauna Management'),
            ('Biosecurity And Pest Management', 'Biosecurity And Pest Management'),
            ('Dust Management', 'Dust Management'),
            ('Reporting', 'Reporting'),
            ('Noise Management', 'Noise Management'),
            ('Erosion And Sedimentation Management', 'Erosion And Sedimentation Management'),
            ('Hazardous Substances And Hydrocarbon Management', 'Hazardous Substances And Hydrocarbon Management'),
            ('Waste Management', 'Waste Management'),
            ('Artificial Light Management', 'Artificial Light Management'),
            ('Audits And Inspections', 'Audits And Inspections'),
            ('Design And Construction Requirements', 'Design And Construction Requirements'),
            ('Regulatory Compliance Reporting', 'Regulatory Compliance Reporting'),
            ('Other', 'Other')
        ]
    )
    custom_environmental_aspect: Optional[str] = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="If 'Other' is selected for Environmental Aspect, please specify the custom aspect here"
    )
    obligation: str = models.TextField()
    accountability: str = models.CharField(
        max_length=255,
        choices=[
            ('Perdaman', 'Perdaman'),
            ('SCJV', 'SCJV'),
            ('SCJV-during construction', 'SCJV-during construction'),
            ('Perdaman-during operations', 'Perdaman-during operations')
        ]
    )
    responsibility: str = models.CharField(
        max_length=255,
        choices=get_responsibility_choices(),
    )
    project_phase: Optional[str] = models.CharField(
        max_length=255,
        null=True,
        choices=[
            ('Pre-Construction', 'Pre-Construction'),
            ('Construction', 'Construction'),
            ('Operation', 'Operation'),
            ('Decommissioning', 'Decommissioning'),
            ('Post-Closure', 'Post-Closure'),
            ('Other', 'Other')
        ]
    )
    action_due_date: Optional[models.DateField] = models.DateField(null=True)
    close_out_date: Optional[models.DateField] = models.DateField(null=True, blank=True)
    status: str = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NOT_STARTED
    )
    supporting_information: Optional[str] = models.TextField(blank=True, null=True)
    general_comments: Optional[str] = models.TextField(blank=True, null=True)
    compliance_comments: Optional[str] = models.TextField(blank=True, null=True)
    non_conformance_comments: Optional[str] = models.TextField(blank=True, null=True)
    evidence_notes = models.TextField(blank=True, null=True,
                                      help_text='Notes about the uploaded evidence')
    recurring_obligation = models.BooleanField(default=False)
    recurring_frequency: Optional[str] = models.CharField(
        max_length=50,
        null=True,
        choices=[
            ('Daily', 'Daily'),
            ('Weekly', 'Weekly'),
            ('Fortnightly', 'Fortnightly'),
            ('Monthly', 'Monthly'),
            ('Quarterly', 'Quarterly'),
            ('Annually', 'Annually'),
            ('Bi-Annually', 'Bi-Annually'),
            ('As Required', 'As Required'),
            ('Mobilisation', 'Mobilisation'),
            ('Decommissioning', 'Decommissioning'),
            ('Extreme Weather', 'Extreme Weather'),
        ]
    )
    recurring_status: Optional[str] = models.CharField(
        max_length=50,
        default='not started',
        null=True,
        choices=[
            ('not started', 'Not Started'),
            ('in progress', 'In Progress'),
            ('completed', 'Completed'),
            ('overdue', 'Overdue'),
        ],
    )
    recurring_forcasted_date: Optional[models.DateField] = models.DateField(blank=True, null=True)
    inspection = models.BooleanField(default=False)
    inspection_frequency: Optional[str] = models.CharField(
        max_length=50,
        null=True,
        choices=[
            ('Daily', 'Daily'),
            ('Weekly', 'Weekly'),
            ('Fortnightly', 'Fortnightly'),
            ('Monthly', 'Monthly'),
            ('Quarterly', 'Quarterly'),
            ('Annually', 'Annually'),
        ]
    )
    site_or_desktop: Optional[str] = models.CharField(
        max_length=10,
        choices=[('Site', 'Site'), ('Desktop', 'Desktop')],
        null=True
    )
    new_control_action_required: bool = models.BooleanField(default=False)
    obligation_type: Optional[str] = models.CharField(
        max_length=50,
        null=True,
        choices=[
            ('Training', 'Training'),
            ('Monitoring', 'Monitoring'),
            ('Reporting', 'Reporting'),
            ('Site based', 'Site based'),
            ('Incident response', 'Incident response'),
            ('Plant mobilisation', 'Plant mobilisation'),
            ('Consultations', 'Consultations'),
            ('Design', 'Design'),
            ('Procurement', 'Procurement'),
            ('Safety', 'Safety'),
        ]
    )
    gap_analysis: Optional[bool] = models.BooleanField(default=False)
    notes_for_gap_analysis: Optional[str] = models.TextField(blank=True, null=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Obligation'
        verbose_name_plural = 'Obligations'
        ordering = ['obligation_number']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['action_due_date']),
            models.Index(fields=['project'])
        ]

    def __str__(self) -> str:
        return f'{self.obligation_number} - {self.project.name}'

    def calculate_next_recurring_date(self) -> Optional[date]:
        """
        Calculate the next recurring date based on frequency and current/last date.

        Returns:
            date: The next forecasted date or None if not applicable
        """
        # If not recurring or no frequency, don't calculate
        if not self.recurring_obligation or not self.recurring_frequency:
            return None

        # Start from last forecasted date, due date, or today
        base_date = self.recurring_forcasted_date or self.action_due_date or timezone.now().date()

        # If base date is in the past, start from today
        today = timezone.now().date()
        if base_date < today:
            base_date = today

        # Normalize frequency
        normalized_frequency = normalize_frequency(self.recurring_frequency)

        # Calculate next date based on frequency
        if normalized_frequency == FREQUENCY_DAILY:
            return base_date + relativedelta(days=1)
        elif normalized_frequency == FREQUENCY_WEEKLY:
            return base_date + relativedelta(weeks=1)
        elif normalized_frequency == FREQUENCY_FORTNIGHTLY:
            return base_date + relativedelta(weeks=2)
        elif normalized_frequency == FREQUENCY_MONTHLY:
            return base_date + relativedelta(months=1)
        elif normalized_frequency == FREQUENCY_QUARTERLY:
            return base_date + relativedelta(months=3)
        elif normalized_frequency == FREQUENCY_BIANNUAL:
            return base_date + relativedelta(months=6)
        elif normalized_frequency == FREQUENCY_ANNUAL:
            return base_date + relativedelta(years=1)
        else:
            # Default to monthly if we don't recognize the frequency
            logger.warning(f"Unrecognized frequency '{self.recurring_frequency}' - defaulting to monthly")
            return base_date + relativedelta(months=1)

    def update_recurring_forecasted_date(self) -> bool:
        """
        Update the recurring forecasted date based on frequency and current status.

        Returns:
            bool: True if the date was updated, False otherwise
        """
        # Skip if not recurring
        if not self.recurring_obligation:
            return False

        next_date = self.calculate_next_recurring_date()

        # Check if the date changed
        if next_date != self.recurring_forcasted_date:
            self.recurring_forcasted_date = next_date
            return True

        return False

    @classmethod
    def get_next_obligation_number(cls) -> str:
        """
        Generate the next sequential obligation number in the format PCEMP-XXX.

        Returns:
            str: The next obligation number (e.g., PCEMP-101)
        """
        prefix = 'PCEMP-'

        # Extract the highest numeric value from all obligation numbers
        highest_number = 0

        # Query all obligation numbers
        all_obligations = cls.objects.all()

        for obligation in all_obligations:
            if obligation.obligation_number and obligation.obligation_number.startswith(prefix):
                try:
                    # Extract numeric part after the prefix
                    number_part = obligation.obligation_number[len(prefix):]
                    current_number = int(number_part)

                    # Update highest if we found a larger number
                    if current_number > highest_number:
                        highest_number = current_number
                except (ValueError, IndexError):
                    # Skip if we can't parse the number
                    continue

        # Increment by 1 for the next number
        next_number = highest_number + 1

        # Format with leading zeros (e.g., PCEMP-001)
        return f'{prefix}{next_number:03d}'

    def clean(self) -> None:
        """Validate the obligation number format."""
        super().clean()

        # Only validate if obligation_number is already set
        # This allows new records to pass validation before the number is generated
        if self.obligation_number and self.obligation_number.strip():
            if not re.match(r'^PCEMP-\d+$', self.obligation_number):
                raise ValidationError({
                    'obligation_number': 'Obligation number must be in the format PCEMP-XXX where XXX is a number'
                })

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save to update mechanism counts and ensure proper obligation number format."""
        # Generate a new obligation number if one isn't provided
        if not self.obligation_number or self.obligation_number.strip() == '':
            self.obligation_number = self.get_next_obligation_number()

        # Ensure the format is correct (prefix + number)
        if not self.obligation_number.startswith('PCEMP-'):
            self.obligation_number = f"PCEMP-{self.obligation_number.split('-')[-1] if '-' in self.obligation_number else self.obligation_number}"

        super().save(*args, **kwargs)

        # Update mechanism counts
        if self.primary_environmental_mechanism:
            self.primary_environmental_mechanism.update_obligation_counts()

    @property
    def is_overdue(self):
        """Check if obligation is overdue."""
        from django.utils import timezone
        if self.status != 'completed' and self.action_due_date:
            return self.action_due_date < timezone.now().date()
        return False

# Signal handlers to update mechanism counts
@receiver(post_save, sender=Obligation)
def update_mechanism_counts_on_save(sender, instance, **kwargs):
    """Update mechanism counts when an obligation is saved."""
    try:
        if instance.primary_environmental_mechanism:
            instance.primary_environmental_mechanism.update_obligation_counts()
            logger.info(
                f'Updated counts for mechanism {instance.primary_environmental_mechanism.name}'
            )
    except Exception as e:
        logger.error(f'Error updating mechanism counts on save: {str(e)}')

@receiver(post_delete, sender=Obligation)
def update_mechanism_counts_on_delete(sender, instance, **kwargs):
    """Update mechanism counts when an obligation is deleted."""
    if instance.primary_environmental_mechanism:
        instance.primary_environmental_mechanism.update_obligation_counts()

class ObligationEvidence(models.Model):
    """Model to store multiple evidence files for an obligation."""
    obligation = models.ForeignKey('Obligation', on_delete=models.CASCADE, related_name='evidences')
    file = models.FileField(
        upload_to='evidence_files/%Y/%m/%d/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg', 'jpeg', 'gif', 'txt', 'csv']
            )
        ],
        max_length=255,
        help_text='Upload evidence documents (25MB max)'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Evidence File'
        verbose_name_plural = 'Evidence Files'

    def __str__(self):
        return f'Evidence for {self.obligation} - {self.file.name}'

    def file_size(self):
        """Return the file size in a human-readable format."""
        size = self.file.size
        if size < 1024:
            return f'{size} bytes'
        elif size < 1024 * 1024:
            return f'{size/1024:.1f} KB'
        else:
            return f'{size/(1024*1024):.1f} MB'

@receiver(pre_save, sender='obligations.Obligation')
def update_forecasted_date_on_change(sender, instance, **kwargs):
    """
    Signal handler to update forecasted date when relevant fields change.
    """
    # If this is a new instance, skip this check
    if not instance.pk:
        # For new instances, just make sure the date is calculated
        instance.update_recurring_forecasted_date()
        return

    try:
        # Get the existing record to compare changes
        old_instance = sender.objects.get(pk=instance.pk)

        # Check if relevant fields changed
        if (instance.recurring_obligation != old_instance.recurring_obligation or
                instance.recurring_frequency != old_instance.recurring_frequency or
                instance.status != old_instance.status or
                instance.action_due_date != old_instance.action_due_date):

            instance.update_recurring_forecasted_date()

        # If status changed to completed, handle recurring logic
        if (instance.status == STATUS_COMPLETED and old_instance.status != STATUS_COMPLETED and
                instance.recurring_obligation):
            # When a recurring obligation is completed, reset status and calculate next date
            instance.status = STATUS_NOT_STARTED
            instance.update_recurring_forecasted_date()

    except sender.DoesNotExist:
        # This shouldn't happen but just in case
        pass

@receiver(pre_save, sender='obligations.Obligation')
def ensure_obligation_number(sender, instance, **kwargs):
    """
    Ensure obligation has a valid number before saving.
    If it's a new record without a number, generate one.
    """
    if not instance.pk and (not instance.obligation_number or instance.obligation_number.strip() == ''):
        instance.obligation_number = Obligation.get_next_obligation_number()
