from typing import TYPE_CHECKING
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from datetime import date
from utils.constants import STATUS_CHOICES
import logging

if TYPE_CHECKING:
    from .models import Obligation  # Forward reference
    User = get_user_model()

logger = logging.getLogger(__name__)

class Project(models.Model):
    """Represents a project entity with related obligations."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.name

    @property
    def obligations(self) -> 'QuerySet[Obligation]':
        """Returns all obligations for this project."""
        return self.project_obligations.all()  # type: ignore

    def get_active_obligations(self) -> 'QuerySet[Obligation]':
        """Returns obligations that are not completed."""
        return self.project_obligations.exclude(status='completed')  # type: ignore

    def get_completed_obligations(self) -> 'QuerySet[Obligation]':
        """Returns completed obligations."""
        return self.project_obligations.filter(status='completed')  # type: ignore

    def get_overdue_obligations(self) -> 'QuerySet[Obligation]':
        """Returns overdue obligations."""
        today = date.today()
        return self.project_obligations.filter(  # type: ignore
            action_due_date__lt=today,
            status__in=['not started', 'in progress']
        )

    def save(self, *args, **kwargs):
        try:
            logger.info(f"Saving project: {self.name}")
            super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving project {self.name}: {str(e)}")
            raise

class Obligation(models.Model):
    """Represents an environmental obligation."""
    obligation_number = models.CharField(max_length=20, primary_key=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_obligations'
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
    recurring_forcasted_date = models.DateField(null=True, blank=True)
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
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Obligation'
        verbose_name_plural = 'Obligations'
        ordering = ['action_due_date', 'obligation_number']

    def __str__(self) -> str:
        return f"{self.obligation_number} - {self.primary_environmental_mechanism}"

    def is_overdue(self) -> bool:
        """Check if obligation is overdue."""
        if not self.action_due_date:
            return False
        return (
            self.action_due_date < date.today() and
            self.status in ['not started', 'in progress']
        )

    def get_status_display_class(self) -> str:
        """Get CSS class for status display."""
        return {
            'not started': 'error',
            'in progress': 'warning',
            'completed': 'success'
        }.get(self.status, '')