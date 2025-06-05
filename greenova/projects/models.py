# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Project models for the projects app.

This module provides the Project, ProjectMembership, and ProjectObligation models,
with strict type annotations, runtime type checking, and Protocol Buffer integration.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protobuf3 integration for project models
    - Lifecycle hooks for membership management

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging

from beartype import beartype
from core.utils.roles import ProjectRole
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django_lifecycle import (
    BEFORE_SAVE,
    AFTER_SAVE,
    AFTER_DELETE,
    LifecycleModel,
    hook,
)
from slugify import slugify

from .commons import PROJECT_ROLE_CHOICES
from .constants import PROJECT_ROLE_CHOICES
from .validators import validate_project_name
from .types import (
    ProjectMetadataDict,
    ProjectMembershipDict,
    ProjectObligationDict,
    ProjectManager,
    MembershipManager,
    ObligationRelationshipHandler,
)

try:
    from pb_model.models import ProtoBufMixin
except ImportError:
    ProtoBufMixin = models.Model  # fallback for type checking

try:
    from .proto.projects_pb2 import (
        ProjectMembershipProto,
        ProjectObligationProto,
        ProjectProto,
    )
except ImportError:
    ProjectProto = None
    ProjectMembershipProto = None
    ProjectObligationProto = None

logger = logging.getLogger(__name__)

User = get_user_model()


@beartype
class Project(LifecycleModel, ProtoBufMixin):
    """Project model to group obligations.

    Attributes:
        pb_model: The protobuf model associated with the Project.
        name: The name of the project.
        slug: The slug for the project, generated from the name.
        description: A text description of the project.
        members: A many-to-many relationship to users through ProjectMembership.
        created_at: The datetime when the project was created.
        updated_at: The datetime when the project was last updated.
    """

    pb_model = ProjectProto

    name = models.CharField(max_length=200, validators=[validate_project_name])
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(
        User,
        through="ProjectMembership",
        related_name="projects",
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["-created_at"]
        permissions = [
            ("view_project", "Can view project"),
            ("change_project", "Can change project"),
            ("delete_project", "Can delete project"),
            ("manage_members", "Can manage project members"),
        ]
        default_permissions = ("add", "change", "delete", "view")

    @beartype
    def __str__(self) -> str:
        """Return the string representation of the Project.

        Returns:
            str: The project name.
        """
        return self.name

    @hook(BEFORE_SAVE)
    @beartype
    def set_slug(self) -> None:
        """Set slug from name if not already set."""
        if not self.slug:
            self.slug = slugify(self.name)

    @beartype
    def get_member_count(self) -> int:
        """Get count of project members.

        Returns:
            int: The number of members in the project.
        """
        return self.members.count()

    @beartype
    def get_user_role(self, user: AbstractUser) -> str:
        """Get user's role in project.

        Args:
            user: The user to check role for.

        Returns:
            str: Role name or 'viewer' if no explicit role found.
        """
        try:
            membership = ProjectMembership.objects.get(project=self, user=user)
            logger.debug(
                "Found role %s for user %s in project %s",
                membership.role,
                user,
                self.name,
            )
            return membership.role
        except ProjectMembership.DoesNotExist:
            logger.debug("No membership found for user %s in project %s", user, self.name)
            return ProjectRole.VIEWER.value
        except Exception as e:
            logger.exception("Error getting user role: %s", str(e))
            return ProjectRole.VIEWER.value

    @beartype
    def has_member(self, user: AbstractUser) -> bool:
        """Check if user is a member of the project.

        Args:
            user: The user to check membership for.

        Returns:
            bool: True if the user is a member, False otherwise.
        """
        return ProjectMembership.objects.filter(project=self, user=user).exists()

    @beartype
    def add_member(
        self,
        user: AbstractUser,
        role: str = ProjectRole.MEMBER.value,
    ) -> None:
        """Add a user to the project with specified role.

        Args:
            user: The user to add to the project.
            role: The role to assign to the user. Defaults to 'member'.
        """
        if not self.has_member(user):
            ProjectMembership.objects.create(
                project=self,
                user=user,
                role=role,
            )
            logger.info("Added user %s to project %s with role %s", user, self.name, role)

    @beartype
    def remove_member(self, user: AbstractUser) -> None:
        """Remove a user from the project.

        Args:
            user: The user to remove from the project.
        """
        ProjectMembership.objects.filter(
            project=self,
            user=user,
        ).delete()
        logger.info("Removed user %s from project %s", user, self.name)

    @beartype
    def get_members_by_role(self, role: str) -> QuerySet[AbstractUser]:
        """Get all users with specified role.

        Args:
            role: The role to filter members by.

        Returns:
            QuerySet[AbstractUser]: A queryset of users with the specified role.
        """
        return User.objects.filter(
            project_memberships__project=self,
            project_memberships__role=role,
        )

    @property
    @beartype
    def obligations(self) -> QuerySet:
        """Get related obligations.

        Returns:
            QuerySet: A queryset of obligations related to the project.
        """
        from obligations.models import Obligation
        return Obligation.objects.filter(project=self)


@beartype
class ProjectMembership(LifecycleModel, ProtoBufMixin):
    """Through model for project memberships.

    Attributes:
        pb_model: The protobuf model associated with the ProjectMembership.
        user: The user associated with the membership.
        project: The project associated with the membership.
        role: The role of the user in the project.
        created_at: The datetime when the membership was created.
        updated_at: The datetime when the membership was last updated.
    """

    pb_model = ProjectMembershipProto

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="project_memberships",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(
        max_length=20,
        choices=PROJECT_ROLE_CHOICES,
        default=PROJECT_ROLE_CHOICES[-1][0],
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "project"]
        ordering = ["project", "user"]
        verbose_name = "Project Membership"
        verbose_name_plural = "Project Memberships"

    @hook(AFTER_SAVE)
    @beartype
    def after_save_membership_lifecycle(self) -> None:
        """Lifecycle hook: called after saving a project membership."""
        logger = logging.getLogger(__name__)
        logger.info(
            "ProjectMembership %s saved (lifecycle hook, replaces signal)",
            self,
        )
        # Add additional event-driven logic here as needed

    @hook(AFTER_DELETE)
    @beartype
    def after_delete_membership_lifecycle(self) -> None:
        """Lifecycle hook: called after deleting a project membership."""
        logger = logging.getLogger(__name__)
        logger.info(
            "ProjectMembership %s deleted (lifecycle hook, replaces signal)",
            self,
        )
        # Add additional cleanup or notification logic here as needed

    @beartype
    def __str__(self) -> str:
        """Return the string representation of the ProjectMembership.

        Returns:
            str: The user-project-role string.
        """
        return f"{self.user.username} - {self.project.name} ({self.role})"


@beartype
class ProjectObligation(ProtoBufMixin):
    """Through model for project obligations.

    Attributes:
        pb_model: The protobuf model associated with the ProjectObligation.
        project: The project associated with the obligation.
        obligation: The obligation associated with the project.
        created_at: The datetime when the obligation was created.
        updated_at: The datetime when the obligation was last updated.
    """

    pb_model = ProjectObligationProto

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project_obligations",
    )
    obligation = models.ForeignKey(
        "obligations.Obligation",
        on_delete=models.CASCADE,
        related_name="project_obligations",
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["project", "obligation"]
        ordering = ["project", "obligation"]
        verbose_name = "Project Obligation"
        verbose_name_plural = "Project Obligations"

    @beartype
    def __str__(self) -> str:
        """Return string representation of ProjectObligation.

        Returns:
            str: The project-obligation string.
        """
        return f"{self.project.name} - {self.obligation.obligation_number}"
