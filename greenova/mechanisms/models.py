from django.db import models
from django.utils import timezone
from django_matplotlib.fields import MatplotlibFigureField
from obligations.constants import STATUS_CHOICES, STATUS_COMPLETED, STATUS_IN_PROGRESS, STATUS_NOT_STARTED
from obligations.utils import is_obligation_overdue

class EnvironmentalMechanism(models.Model):
    """Represents an environmental mechanism that governs obligations."""
    name = models.CharField(max_length=255)
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='mechanisms'
    )
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    effective_date = models.DateField(null=True, blank=True)

    # Add status field
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NOT_STARTED
    )

    # Add count fields
    not_started_count = models.IntegerField(default=0)
    in_progress_count = models.IntegerField(default=0)
    completed_count = models.IntegerField(default=0)
    overdue_count = models.IntegerField(default=0)  # Add overdue count

    primary_environmental_mechanism = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add matplotlib figure fields
    status_chart = MatplotlibFigureField(
        figure='get_mechanism_chart',
        plt_args=lambda obj: (obj.id,),
        fig_width=300,
        fig_height=250,
        output_format='png',
        silent=True
    )

    class Meta:
        verbose_name = 'Environmental Mechanism'
        verbose_name_plural = 'Environmental Mechanisms'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def total_obligations(self) -> int:
        """Total number of obligations."""
        return self.not_started_count + self.in_progress_count + self.completed_count

    def update_obligation_counts(self):
        """Update obligation counts based on related obligations."""
        from obligations.models import Obligation

        # Get all related obligations
        obligations = Obligation.objects.filter(primary_environmental_mechanism=self)

        # Reset counts
        self.not_started_count = 0
        self.in_progress_count = 0
        self.completed_count = 0
        self.overdue_count = 0

        # Count obligations by status
        for obligation in obligations:
            status = obligation.status

            # Check if overdue using the utility function
            if is_obligation_overdue(obligation):
                self.overdue_count += 1

            # Also count by regular status
            if status == STATUS_NOT_STARTED:
                self.not_started_count += 1
            elif status == STATUS_IN_PROGRESS:
                self.in_progress_count += 1
            elif status == STATUS_COMPLETED:
                self.completed_count += 1

        self.save()

    def get_status_data(self):
        """Return a dictionary of status counts for charting."""
        return {
            'Overdue': self.overdue_count,
            'Not Started': max(0, self.not_started_count - self.overdue_count),
            'In Progress': self.in_progress_count,
            'Completed': self.completed_count
        }
