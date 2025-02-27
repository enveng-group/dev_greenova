from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from projects.models import Project
from typing import Any, Dict, List, Optional, Tuple, Type, Union
import logging
import re

logger = logging.getLogger(__name__)

class Obligation(models.Model):
    """Represents an environmental obligation."""
    obligation_number = models.CharField(
        max_length=20,
        primary_key=True,
        help_text="Format: PCEMP-XXX where XXX is a number"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='obligations'
    )
    # Change ForeignKey to string reference
    primary_environmental_mechanism = models.ForeignKey(
        'mechanisms.EnvironmentalMechanism',
        on_delete=models.PROTECT,
        related_name='obligations',
        null=True,
        verbose_name='Environmental Mechanism'
    )
    procedure = models.TextField(blank=True, null=True)
    environmental_aspect = models.CharField(max_length=255,
        choices =[
            ('Air', 'Air'),
            ('Water', 'Water'),
            ('Waste', 'Waste'),
            ('Energy', 'Energy'),
            ('Biodiversity', 'Biodiversity'),
            ('Noise', 'Noise'),
            ('Chemicals', 'Chemicals'),
            ('Soil', 'Soil'),
            ('Other', 'Other')
        ]
        )
    obligation = models.TextField()
    accountability = models.CharField(max_length=255)
    responsibility = models.CharField(max_length=255)
    project_phase = models.CharField(max_length=255, blank=True, null=True,
        choices=[
            ('Pre-Construction', 'Pre-Construction'),
            ('Construction', 'Construction'),
            ('Operation', 'Operation'),
            ('Decommissioning', 'Decommissioning'),
            ('Post-Closure', 'Post-Closure'),
            ('Other', 'Other')
        ]
        )
    action_due_date = models.DateField(null=True, blank=True)
    close_out_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('not started', 'Not Started'),
            ('in progress', 'In Progress'),
            ('completed', 'Completed')
        ],
        default='not started'
    )
    supporting_information = models.TextField(blank=True, null=True)
    general_comments = models.TextField(blank=True, null=True)
    compliance_comments = models.TextField(blank=True, null=True)
    non_conformance_comments = models.TextField(blank=True, null=True)
    evidence = models.TextField(blank=True, null=True)
    person_email = models.EmailField(blank=True, null=True)
    recurring_obligation = models.BooleanField(default=False)
    recurring_frequency = models.CharField(max_length=50, blank=True, null=True)
    recurring_status = models.CharField(max_length=50, blank=True, null=True)
    recurring_forcasted_date = models.DateField(blank=True, null=True)
    inspection = models.BooleanField(default=False)
    inspection_frequency = models.CharField(max_length=50, blank=True, null=True)
    site_or_desktop = models.CharField(
        max_length=10,
        choices=[('Site', 'Site'), ('Desktop', 'Desktop')],
        blank=True,
        null=True
    )
    new_control_action_required = models.BooleanField(default=False)
    obligation_type = models.CharField(max_length=50, blank=True, null=True)
    gap_analysis = models.TextField(blank=True, null=True)
    notes_for_gap_analysis = models.TextField(blank=True, null=True)
    covered_in_which_inspection_checklist = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Specifies which inspection checklist covers this obligation"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Obligation'
        verbose_name_plural = 'Obligations'
        ordering = ['action_due_date', 'obligation_number']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['action_due_date']),
            models.Index(fields=['project'])
        ]

    def __str__(self) -> str:
        return f"{self.obligation_number}"

        @classmethod
        def get_next_obligation_number(cls) -> str:
            """
            Generate the next available obligation number in the format PCEMP-XXX.

            Returns:
                str: The next available obligation number
            """
            # Get the prefix
            prefix = "PCEMP-"

            # Find the highest number with this prefix
            last_obligation = cls.objects.filter(
                obligation_number__startswith=prefix
            ).order_by('-obligation_number').first()

            if last_obligation:
                # Extract the number from the last obligation
                match = re.search(r'PCEMP-(\d+)', last_obligation.obligation_number)
                if match:
                    last_number = int(match.group(1))
                    next_number = last_number + 1
                else:
                    # If for some reason the format is wrong, start from 1
                    next_number = 1
            else:
                # No existing obligations, start from 1
                next_number = 1

            # Format the new obligation number with leading zeros
            # For example: PCEMP-001, PCEMP-002, ..., PCEMP-999
            return f"{prefix}{next_number:03d}"

        def clean(self) -> None:
            """Validate the obligation number format."""
            super().clean()

            from django.core.exceptions import ValidationError
            # Check if the obligation number follows the required format
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


    # Signal handlers to update mechanism counts
    @receiver(post_save, sender=obligation)
    def update_mechanism_counts_on_save(sender: Type[obligation], instance: obligation, **kwargs: Any) -> None:
        """Update mechanism counts when an obligation is saved."""
        if instance.primary_environmental_mechanism:
            instance.primary_environmental_mechanism.update_obligation_counts()

    @receiver(post_delete, sender=obligation)
    def update_mechanism_counts_on_delete(sender: Type[obligation], instance: obligation, **kwargs: Any) -> None:
        """Update mechanism counts when an obligation is deleted."""
        if instance.primary_environmental_mechanism:
            instance.primary_environmental_mechanism.update_obligation_counts()
