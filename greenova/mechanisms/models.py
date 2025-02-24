from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from projects.models import Project
from typing import Dict, Any
import logging
from utils.relationship_manager import relationship_manager

logger = logging.getLogger(__name__)

class ChartConfiguration(models.Model):
    """Configuration for mechanism chart displays."""

    CHART_TYPES = [
        ('polar', 'Polar Area'),
        ('bar', 'Bar Chart'),
        ('pie', 'Pie Chart'),
        ('doughnut', 'Doughnut Chart')
    ]

    mechanism = models.OneToOneField(
        'EnvironmentalMechanism',
        on_delete=models.CASCADE,
        related_name='chart_config'
    )
    chart_type = models.CharField(
        max_length=20,
        choices=CHART_TYPES,
        default='polar'
    )
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'created_at']

    def __str__(self) -> str:
        return f"{self.mechanism.name} Chart Config"

    def get_chart_config(self) -> Dict[str, Any]:
        """Generate Chart.js configuration."""
        return {
            'type': self.chart_type,
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'plugins': {
                    'legend': {
                        'position': 'right'
                    }
                }
            }
        }

# Update EnvironmentalMechanism model

class EnvironmentalMechanism(models.Model):
    """Represents an environmental mechanism."""

    name = models.CharField(max_length=255)
    project = relationship_manager.create_foreign_key(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='mechanisms'
    )
    description = models.TextField(blank=True, null=True)
    not_started_count = models.IntegerField(default=0)
    in_progress_count = models.IntegerField(default=0)
    completed_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=[
        ('not started', 'Not Started'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed')
    ])
    updated_at = models.DateTimeField(auto_now=True)  # Add this field

    class Meta:
        ordering = ['name', '-updated_at']
        # Add unique together constraint
        unique_together = ['name', 'project']

    def __str__(self) -> str:
        return self.name

    def get_chart_data(self) -> Dict[str, Any]:
        """Get chart data for this mechanism."""
        STATUS_CHOICES = [
            ('not started', 'Not Started'),
            ('in progress', 'In Progress'),
            ('completed', 'Completed')
        ]
        status_counts = {status: 0 for status, _ in STATUS_CHOICES}
        status_counts[self.status] = 1

        return {
            'labels': [label for _, label in STATUS_CHOICES],
            'datasets': [{
                'data': list(status_counts.values()),
                'backgroundColor': [
                    '#FF6384',  # Red for not started
                    '#36A2EB',  # Blue for in progress
                    '#FFCE56'   # Yellow for completed
                ]
            }]
        }

    def clean(self) -> None:
        """Validate mechanism data."""
        super().clean()
        if not self.name:
            raise ValidationError({'name': 'Name is required'})
        if not self.project:
            raise ValidationError({'project': 'Project is required'})

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Save mechanism and ensure chart config exists."""
        self.full_clean()
        super().save(*args, **kwargs)
        # Create default chart config if none exists
        ChartConfiguration.objects.get_or_create(
            mechanism=self,
            defaults={'chart_type': 'polar'}
        )

    def get_related_obligations(self):
        """Get all obligations related to this mechanism."""
        from obligations.models import Obligation
        return Obligation.objects.filter(
            primary_environmental_mechanism=self
        )

    def update_status_from_obligations(self):
        """Update mechanism status based on related obligations."""
        obligations = self.get_related_obligations()
        if not obligations.exists():
            return

        total = obligations.count()
        completed = obligations.filter(status='completed').count()

        if completed == 0:
            self.status = 'not started'
        elif completed == total:
            self.status = 'completed'
        else:
            self.status = 'in progress'

        self.save()

    def update_status_counts(self):
        """Update counts for each status from related obligations."""
        obligations = self.get_related_obligations()

        self.not_started_count = obligations.filter(status='not started').count()
        self.in_progress_count = obligations.filter(status='in progress').count()
        self.completed_count = obligations.filter(status='completed').count()

        # Update overall status based on counts
        total = self.not_started_count + self.in_progress_count + self.completed_count

        if total == 0:
            self.status = 'not started'
        elif self.completed_count == total:
            self.status = 'completed'
        elif self.in_progress_count > 0 or self.completed_count > 0:
            self.status = 'in progress'
        else:
            self.status = 'not started'

        self.save()

    @property
    def total_obligations(self):
        """Get total number of obligations."""
        return self.not_started_count + self.in_progress_count + self.completed_count
