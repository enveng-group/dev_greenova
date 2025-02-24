from django.db import models


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
