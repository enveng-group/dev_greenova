import logging
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Count
from enum import Enum
from typing import Dict, Any, List
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

User = get_user_model()

if TYPE_CHECKING:
    from django.contrib.auth.models import User

class ProjectRole(str, Enum):
    """Project role types."""
    OWNER = 'owner'
    MANAGER = 'manager'
    MEMBER = 'member'
    VIEWER = 'viewer'

    @classmethod
    def choices(cls) -> List[tuple[str, str]]:
        """Get choices for model field."""
        return [(role.value, role.value.title()) for role in cls]

class Project(models.Model):
    """Project model to group obligations."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(
        User,
        through='ProjectMembership',
        related_name='projects'
    )
    members = models.ManyToManyField(
        User,
        through='ProjectMembership',
        related_name='projects'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Add type hints for reverse relations
    memberships: models.Manager['ProjectMembership']

    if TYPE_CHECKING:
        obligations: models.Manager['Obligation']

    def get_all_obligations(self) -> models.QuerySet['Obligation']:
        """Get all obligations for this project."""
        from obligations.models import Obligation
        return Obligation.objects.filter(project=self)

    def get_completed_obligations(self) -> models.QuerySet['Obligation']:
        """Get completed obligations for this project."""
        from obligations.models import Obligation
        return Obligation.objects.filter(project=self, status='completed')

    def get_active_obligations(self) -> models.QuerySet['Obligation']:
        """Get active obligations for this project."""
        from obligations.models import Obligation
        return Obligation.objects.filter(project=self, status='in progress')

    def get_overdue_obligations(self) -> models.QuerySet['Obligation']:
        """Get overdue obligations for this project."""
        from obligations.models import Obligation
        return Obligation.objects.filter(
            project=self,
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

def get_member_count(self) -> int:
    """Get count of project members."""
    return self.members.count()

class Meta:
    verbose_name = 'Project'
    verbose_name_plural = 'Projects'
    ordering = ['-created_at']

def get_all_obligations(self) -> models.QuerySet['Obligation']:
    """Get all obligations for this project."""
    from obligations.models import Obligation
    return Obligation.objects.filter(project=self)

def get_completed_obligations(self) -> models.QuerySet['Obligation']:
    """Get completed obligations for this project."""
    from obligations.models import Obligation
    return Obligation.objects.filter(project=self, status='completed')

def get_active_obligations(self) -> models.QuerySet['Obligation']:
    """Get active obligations for this project."""
    from obligations.models import Obligation
    return Obligation.objects.filter(project=self, status='in progress')

def get_overdue_obligations(self) -> models.QuerySet['Obligation']:
    """Get overdue obligations for this project."""
    from obligations.models import Obligation
    return Obligation.objects.filter(
        project=self,
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
    """Get user's role in the project."""
    try:
        membership = self.memberships.get(user=user)
        return membership.role
    except ProjectMembership.DoesNotExist:
        return ProjectRole.VIEWER.value
    except Exception as e:
        logger.error(f"Error getting user role: {str(e)}")
        return ProjectRole.VIEWER.value

def get_user_context(self, user: AbstractUser) -> Dict[str, Any]:
    """Get user-specific context for this project."""
    role = self.get_user_role(user)
    return {
        'role': role,
        'can_edit': role in [ProjectRole.OWNER.value, ProjectRole.MANAGER.value],
        'can_delete': role == ProjectRole.OWNER.value,
        'is_member': True
    }

class ProjectMembership(models.Model):
    user = models.ForeignKey(
        User,
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
created_at = models.DateTimeField(default=timezone.now)
updated_at = models.DateTimeField(auto_now=True)



class Meta:
    verbose_name = 'Project Membership'
    verbose_name_plural = 'Project Memberships'
    unique_together = ['user', 'project']

def __str__(self: 'ProjectMembership') -> str:
    """Return string representation of the project membership."""
    # Type hints are available since self is properly typed
    return f'{self.user.username} - {self.project.name} ({self.role})'
