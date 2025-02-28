import logging
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import QuerySet
from enum import Enum
from typing import List
from django.contrib.auth.models import AbstractUser

logger = logging.getLogger(__name__)

User = get_user_model()


class ProjectRole(str, Enum):
    """Define valid project roles."""
    OWNER = 'owner'
    MANAGER = 'manager'
    MEMBER = 'member'
    VIEWER = 'viewer'
    SIMON = 'simon'

    @classmethod
    def choices(cls) -> List[tuple[str, str]]:
        """Get choices for model field."""
        return [(role.value, role.value.title()) for role in cls]


class Project(models.Model):
    """Project model to group obligations."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(
        User,
        through='ProjectMembership',
        related_name='projects'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.name

    def get_member_count(self) -> int:
        """Get count of project members."""
        return self.members.count()

    def get_user_role(self, user: AbstractUser) -> str:
        """
        Get user's role in project.

        Args:
            user: The user to check role for

        Returns:
            str: Role name or 'viewer' if no explicit role found
        """
        try:
            membership = ProjectMembership.objects.get(project=self, user=user)
            logger.debug(
                f"Found role {membership.role} for user {user} in project {self.name}"
            )
            return membership.role
        except ProjectMembership.DoesNotExist:
            logger.debug(f"No membership found for user {user} in project {self.name}")
            return ProjectRole.VIEWER.value
        except Exception as e:
            logger.error(f"Error getting user role: {str(e)}")
            return ProjectRole.VIEWER.value

    def has_member(self, user: AbstractUser) -> bool:
        """Check if user is a member of the project."""
        return ProjectMembership.objects.filter(project=self, user=user).exists()

    def add_member(
            self,
            user: AbstractUser,
            role: str = ProjectRole.MEMBER.value) -> None:
        """Add a user to the project with specified role."""
        if not self.has_member(user):
            ProjectMembership.objects.create(
                project=self,
                user=user,
                role=role
            )
            logger.info(f"Added user {user} to project {self.name} with role {role}")

    def remove_member(self, user: AbstractUser) -> None:
        """Remove a user from the project."""
        ProjectMembership.objects.filter(
            project=self,
            user=user
        ).delete()
        logger.info(f"Removed user {user} from project {self.name}")

    def get_members_by_role(self, role: str) -> QuerySet[AbstractUser]:
        """Get all users with specified role."""
        return User.objects.filter(
            project_memberships__project=self,
            project_memberships__role=role
        )

    @property
    def obligations(self):
        """Get related obligations."""
        # Move import inside method to avoid circular import
        from obligations.models import Obligation
        return Obligation.objects.filter(project=self)


class ProjectMembership(models.Model):
    """Through model for project memberships."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project_memberships'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    role = models.CharField(
        max_length=20,
        choices=ProjectRole.choices(),
        default=ProjectRole.MEMBER.value
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'project']
        ordering = ['project', 'user']
        verbose_name = 'Project Membership'
        verbose_name_plural = 'Project Memberships'

    def __str__(self) -> str:
        return f"{self.user.username} - {self.project.name} ({self.role})"


class ProjectObligation(models.Model):
    """Through model for project obligations."""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_obligations'
    )
    obligation = models.ForeignKey(
        'obligations.Obligation',
        on_delete=models.CASCADE,
        related_name='project_obligations'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['project', 'obligation']
        ordering = ['project', 'obligation']
        verbose_name = 'Project Obligation'
        verbose_name_plural = 'Project Obligations'

    def __str__(self) -> str:
        """Return string representation of ProjectObligation."""
        return f"{self.project.name} - {self.obligation.obligation_number}"
