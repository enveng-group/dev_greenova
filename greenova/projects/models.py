from typing import TYPE_CHECKING
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from datetime import date
from utils.constants import STATUS_CHOICES
import logging

if TYPE_CHECKING:
    from obligations.models import Obligation  # Updated import path
    User = get_user_model()

logger = logging.getLogger(__name__)

class Project(models.Model):
    """Represents a project entity with related obligations."""
    id = models.AutoField(primary_key=True)  # Add explicit id field
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
        return self.obligations.all()  # Using the related_name from Obligation model

    def get_active_obligations(self) -> 'QuerySet[Obligation]':
        """Get active obligations."""
        return self.obligations.exclude(status='completed')

    def get_completed_obligations(self) -> 'QuerySet[Obligation]':
        """Get completed obligations."""
        return self.obligations.filter(status='completed')

    def get_overdue_obligations(self) -> 'QuerySet[Obligation]':
        """Get overdue obligations."""
        from django.utils import timezone
        return (
            self.obligations
            .filter(
                action_due_date__lt=timezone.now().date(),
                status__in=['not started', 'in progress']
            )
        )

    def get_analytics(self):
        """Get analytics data for the project."""
        return {
            'total_obligations': self.obligations.count(),
            'completed': self.obligations.filter(status='completed').count(),
            'in_progress': self.obligations.filter(status='in progress').count(),
            'not_started': self.obligations.filter(status='not started').count()
        }

    def save(self, *args, **kwargs):
        try:
            logger.info(f"Saving project: {self.name}")
            super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving project {self.name}: {str(e)}")
            raise