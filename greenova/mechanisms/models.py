from django.db import models
from django.utils import timezone

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
        choices=[
            ('not started', 'Not Started'),
            ('in progress', 'In Progress'),
            ('completed', 'Completed')
        ],
        default='not started'
    )

    # Add count fields
    not_started_count = models.IntegerField(default=0)
    in_progress_count = models.IntegerField(default=0)
    completed_count = models.IntegerField(default=0)
    overdue_count = models.IntegerField(default=0)  # Add overdue count

    primary_environmental_mechanism = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

        today = timezone.now().date()

        # Count obligations by status
        for obligation in obligations:
            status = obligation.status

            # Check if overdue (not completed and past due date)
            if (status in ['not started', 'in progress'] and
                obligation.action_due_date and
                obligation.action_due_date < today):
                self.overdue_count += 1

            # Also count by regular status
            if status == 'not started':
                self.not_started_count += 1
            elif status == 'in progress':
                self.in_progress_count += 1
            elif status == 'completed':
                self.completed_count += 1

        self.save()
