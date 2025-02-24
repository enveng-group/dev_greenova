from django.db import models
from utils.relationship_manager import relationship_manager
from utils.constants import STATUS_CHOICES


class Obligation(models.Model):
    """Represents an environmental obligation."""
    obligation_number = models.CharField(max_length=20, primary_key=True)
    project = relationship_manager.create_foreign_key(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='obligations'
    )
    primary_environmental_mechanism = models.CharField(max_length=255)
    procedure = models.TextField(blank=True, null=True)
    environmental_aspect = models.CharField(max_length=255)
    obligation = models.TextField()
    accountability = models.CharField(max_length=255)
    responsibility = models.CharField(max_length=255)
    project_phase = models.CharField(max_length=255, blank=True, null=True)
    action_due_date = models.DateField(null=True, blank=True)
    close_out_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
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
