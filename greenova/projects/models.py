import logging
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.db.models import QuerySet, Count
from enum import Enum
from typing import cast, Dict, Any, Optional
from django.contrib.auth.models import AbstractUser

logger = logging.getLogger(__name__)

User = get_user_model()

class ProjectRole(str, Enum):
    """Project role types."""
    OWNER = 'owner'
    MANAGER = 'manager'
    MEMBER = 'member'
    VIEWER = 'viewer'

    @classmethod
    def choices(cls):
        """Get choices for model field."""
        return [(role.value, role.name.title()) for role in cls]

class Project(models.Model):
    """Represents a project entity."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ProjectMembership',
        related_name='projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add type hints for reverse relations
    memberships: models.Manager['ProjectMembership']

    @property
    def obligations(self) -> models.QuerySet:
        """Get all obligations for this project."""
        from obligations.models import Obligation
        return Obligation.objects.filter(project=self)

    def get_completed_obligations(self) -> models.QuerySet:
        """Get completed obligations for this project."""
        return self.obligations.filter(status='completed')

    def get_active_obligations(self) -> models.QuerySet:
        """Get active obligations for this project."""
        return self.obligations.filter(status='in progress')

    def get_overdue_obligations(self) -> models.QuerySet:
        """Get overdue obligations for this project."""
        return self.obligations.filter(
            action__due_date__lt=timezone.now().date(),
            status__in=['not started', 'in progress']
        )

    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics data for the project."""
        return {
            'total_obligations': self.obligations.count(),
            'status_counts': {
                'not_started': self.obligations.filter(status='Not Started').count(),
                'in_progress': self.obligations.filter(status='In Progress').count(),
                'completed': self.obligations.filter(status='Completed').count(),
            },
            'mechanisms': (self.obligations
                         .values('primary_environmental_mechanism')
                         .annotate(total=Count('id'))
                         .order_by('primary_environmental_mechanism')),
            'aspects': (self.obligations
                       .values('environmental_aspect')
                       .annotate(total=Count('id'))
                       .order_by('environmental_aspect'))
        }

    def get_user_role(self, user: AbstractUser) -> str:
        """Get user's role in the project.
        
        Args:
            user: The user to check
            
        Returns:
            str: Role name or 'no_role' if not found
        """
        try:
            membership = self.memberships.get(user=user)
            return membership.role
        except ProjectMembership.DoesNotExist:
            return ProjectRole.VIEWER.value
        except Exception as e:
            logger.error(f"Error getting user role: {str(e)}")
            return ProjectRole.VIEWER.value

    def get_user_context(self, user: AbstractUser) -> Dict[str, Any]:
        """Get user-specific context for this project.
        
        Args:
            user: The user to get context for
            
        Returns:
            Dict containing user role and permissions
        """
        role = self.get_user_role(user)
        return {
            'role': role,
            'can_edit': role in [ProjectRole.OWNER.value, ProjectRole.MANAGER.value],
            'can_delete': role == ProjectRole.OWNER.value,
            'is_member': True
        }

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-created_at']

class ProjectMembership(models.Model):
    """Handle user membership in projects."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='project_memberships'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='memberships'  # This creates the reverse relation
    )
    role = models.CharField(
        max_length=20,
        choices=ProjectRole.choices(),
        default=ProjectRole.MEMBER.value
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Project Membership'
        verbose_name_plural = 'Project Memberships'
        unique_together = ['user', 'project']