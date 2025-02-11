from accounts.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Obligation(models.Model):
    """Model for environmental obligations tracking."""

    STATUS_CHOICES = [
        ('not started', 'Not Started'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),  # Add overdue status
    ]

    SITE_DESKTOP_CHOICES = [('Site', 'Site'), ('Desktop', 'Desktop')]

    # Primary Fields
    obligation_number = models.CharField(
        max_length=20,
        primary_key=True,
        help_text=_("Unique identifier for the obligation (e.g., PCEMP-01)"),
    )
    project_name = models.CharField(max_length=255)
    primary_environmental_mechanism = models.TextField(blank=True, null=True)
    procedure = models.TextField(blank=True, null=True)
    environmental_aspect = models.TextField(blank=True, null=True)
    obligation = models.TextField()

    # Responsibility Fields
    accountability = models.CharField(max_length=255, blank=True, null=True)
    responsibility = models.CharField(max_length=255, blank=True, null=True)
    project_phase = models.TextField(blank=True, null=True)
    person_email = models.EmailField(max_length=255, blank=True, null=True)

    # Date Fields
    action_due_date = models.DateField(blank=True, null=True)
    close_out_date = models.DateField(blank=True, null=True)

    # Status and Comments
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='not started'
    )
    supporting_information = models.TextField(blank=True, null=True)
    general_comments = models.TextField(blank=True, null=True)
    compliance_comments = models.TextField(blank=True, null=True)
    non_conformance_comments = models.TextField(blank=True, null=True)
    evidence = models.TextField(blank=True, null=True)

    # Recurring Fields
    recurring_obligation = models.BooleanField(default=False)
    recurring_frequency = models.CharField(
        max_length=50, blank=True, null=True
    )
    recurring_status = models.CharField(max_length=50, blank=True, null=True)
    recurring_forcasted_date = models.DateField(blank=True, null=True)

    # Inspection Fields
    inspection = models.BooleanField(default=False)
    inspection_frequency = models.CharField(
        max_length=50, blank=True, null=True
    )
    site_or_desktop = models.CharField(
        max_length=50, choices=SITE_DESKTOP_CHOICES, blank=True, null=True
    )

    # Additional Fields
    new_control_action_required = models.BooleanField(default=False)
    obligation_type = models.CharField(max_length=50, blank=True, null=True)
    gap_analysis = models.TextField(blank=True, null=True)
    notes_for_gap_analysis = models.TextField(blank=True, null=True)
    covered_in_which_inspection_checklist = models.CharField(
        max_length=255, blank=True, null=True
    )

    # Audit Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_obligations',
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_obligations',
    )

    class Meta:
        verbose_name = _('Obligation')
        verbose_name_plural = _('Obligations')
        ordering = ['obligation_number']
        indexes = [
            models.Index(fields=['project_name']),
            models.Index(fields=['status']),
            models.Index(fields=['action_due_date']),
            models.Index(fields=['project_phase']),
        ]

    def __str__(self):
        return f"{self.obligation_number} - {self.project_name}"

    def is_overdue(self):
        """Check if the obligation is overdue."""
        if self.action_due_date and self.status != 'completed':
            return self.action_due_date < timezone.now().date()
        return False

    def save(self, *args, **kwargs):
        """Override save to check for overdue status"""
        if self.action_due_date and self.status != 'completed':
            if self.action_due_date < timezone.now().date():
                self.status = 'overdue'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get the absolute URL for this obligation."""
        from django.urls import reverse

        return reverse(
            'obligations:detail', kwargs={'pk': self.obligation_number}
        )
