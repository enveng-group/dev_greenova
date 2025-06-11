import logging
from typing import ClassVar

from django.db import models
from django.utils import timezone
from projects.models import Project

logger = logging.getLogger(__name__)


class Procedure(models.Model):
    """Model representing environmental procedures and workflows."""

    STATUS_CHOICES: ClassVar[list] = [
        ('draft', 'Draft'),
        ('review', 'In Review'),
        ('active', 'Active'),
        ('obsolete', 'Obsolete'),
        ('archived', 'Archived')
    ]

    COMPLIANCE_STATUSES: ClassVar[list] = [
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('partially_compliant', 'Partially Compliant'),
        ('not_assessed', 'Not Assessed')
    ]

    # Basic information
    name: models.CharField = models.CharField(max_length=255)
    document_id: models.CharField = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique procedure identifier (e.g., ENV-PROC-001)"
    )
    project: models.ForeignKey = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='procedures'
    )
    version: models.CharField = models.CharField(max_length=10, default='1.0')
    description: models.TextField = models.TextField(blank=True)

    # Status and dates
    status: models.CharField = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    compliance_status: models.CharField = models.CharField(
        max_length=20,
        choices=COMPLIANCE_STATUSES,
        default='not_assessed'
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    effective_date: models.DateField = models.DateField(null=True, blank=True)
    review_date: models.DateField = models.DateField(null=True, blank=True)
    completed_at: models.DateTimeField = models.DateTimeField(null=True, blank=True)

    # Document management
    document_file: models.FileField = models.FileField(
        upload_to='procedures/%Y/%m/',
        null=True,
        blank=True
    )

    # Metadata
    is_active: models.BooleanField = models.BooleanField(default=True)
    tags: models.CharField = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Procedure'
        verbose_name_plural = 'Procedures'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['compliance_status']),
            models.Index(fields=['document_id'])
        ]

    def __str__(self) -> str:
        return f"{self.document_id} - {self.name}"

    def mark_as_completed(self) -> None:
        """Mark the procedure as completed with current timestamp."""
        self.completed_at = timezone.now()
        self.save(update_fields=['completed_at'])

    def set_status(self, status: str) -> None:
        """Update the procedure status."""
        if status in dict(self.STATUS_CHOICES):
            self.status = status
            self.save(update_fields=['status', 'updated_at'])
        else:
            logger.warning(
                "Invalid status: %s for procedure %s",
                status,
                self.document_id
            )

    def is_due_for_review(self) -> bool:
        """Check if procedure is due for review."""
        if not self.review_date:
            return False
        return self.review_date <= timezone.now().date()
