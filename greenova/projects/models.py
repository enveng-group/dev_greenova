# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Project models for the projects app.

This module provides the Project, ProjectMembership, and ProjectObligation models,
with strict type annotations, runtime type checking, and Protocol Buffer integration.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Lifecycle hooks for membership management

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging

import bleach
from beartype import beartype
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from slugify import slugify

logger = logging.getLogger(__name__)

User = get_user_model()


class Project(models.Model):
    """Project model to group obligations.

    Attributes:
        name: The name of the project.
        slug: The slug for the project, generated from the name.
        description: A text description of the project.
        owner: The user who owns the project.
        members: A many-to-many relationship to users through ProjectMembership.
        created_at: The datetime when the project was created.
        updated_at: The datetime when the project was last updated.

    """

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        null=True,
        blank=True,
        help_text="The user who owns this project.",
    )
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

    # Slug is now set via pre_save signal in signals.py

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
        membership = self.projectmembership_set.filter(user=user).first()
        if membership:
            return membership.role
        return "viewer"

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
        role: str = "member",
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
            logger.info(
                "Added user %s to project %s with role %s",
                user,
                self.name,
                role,
            )

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

    @beartype
    def to_pb(self) -> "object":  # type: ignore[return]
        """Convert this Project instance to a ProjectProto message.

        Returns:
            ProjectProto: The protocol buffer message representing this project.

        """
        from . import projects_pb2  # type: ignore[import]

        proto = projects_pb2.ProjectProto()  # type: ignore[attr-defined]
        proto.id = str(self.pk) if self.pk is not None else ""
        proto.name = self.name or ""
        proto.description = self.description or ""
        # type: ignore[attr-defined]
        proto.member_user_ids.extend([str(user.pk) for user in self.members.all()])
        proto.created_at = self.created_at.isoformat() if self.created_at else ""
        proto.updated_at = self.updated_at.isoformat() if self.updated_at else ""
        return proto  # type: ignore[return]

    @beartype
    def from_pb(self, proto: object) -> "Project":
        """Populate this Project instance from a ProjectProto message.

        Args:
            proto: The ProjectProto message to populate from (expected type: projects_pb2.ProjectProto).

        Returns:
            Project: The populated Project instance (self).

        """
        # Type: ignore is used because generated proto types are not always
        # visible to type checkers
        self.name = getattr(proto, "name", "")
        self.description = getattr(proto, "description", "")
        # Slug and owner are not set from proto for safety
        # Members are not set here; handle separately if needed
        # created_at/updated_at are not set directly (managed by Django)
        return self

    def save(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        """Override save to sanitize description and ensure slug."""
        if not self.slug:
            self.slug = slugify(self.name)
        self.description = bleach.clean(self.description or "")
        super().save(*args, **kwargs)


class ProjectMembership(models.Model):
    """Through model for project memberships.

    Attributes:
        user: The user associated with the membership.
        project: The project associated with the membership.
        role: The role of the user in the project.
        created_at: The datetime when the membership was created.
        updated_at: The datetime when the membership was last updated.

    """

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
        default="viewer",
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "project"]
        ordering = ["project", "user"]
        verbose_name = "Project Membership"
        verbose_name_plural = "Project Memberships"

    # Membership lifecycle logic is now handled via post_save and post_delete
    # signals in signals.py

    @beartype
    def __str__(self) -> str:
        """Return the string representation of the ProjectMembership.

        Returns:
            str: The user-project-role string.

        """
        return f"{self.user.username} - {self.project.name} ({self.role})"

    @beartype
    def to_pb(self) -> "object":  # type: ignore[return]
        """Convert this ProjectMembership instance to a ProjectMembershipProto message.

        Returns:
            ProjectMembershipProto: The protocol buffer message representing this membership.

        """
        from . import projects_pb2  # type: ignore[import]

        proto = projects_pb2.ProjectMembershipProto()  # type: ignore[attr-defined]
        proto.id = str(self.pk) if self.pk is not None else ""
        proto.project_id = str(self.project.pk) if self.project.pk else ""
        proto.user_id = str(self.user.pk) if self.user.pk else ""
        proto.role = self.role or ""
        proto.created_at = self.created_at.isoformat() if self.created_at else ""
        proto.updated_at = self.updated_at.isoformat() if self.updated_at else ""
        return proto  # type: ignore[return]

    @beartype
    def from_pb(self, proto: object) -> "ProjectMembership":
        """Populate this ProjectMembership instance from a ProjectMembershipProto message.

        Args:
            proto: The ProjectMembershipProto message to populate from (expected type: projects_pb2.ProjectMembershipProto).

        Returns:
            ProjectMembership: The populated ProjectMembership instance (self).

        """
        # Only set fields that are safe to update
        self.role = getattr(proto, "role", "")
        # project, user, created_at, updated_at are not set here (handle in view/logic)
        return self


# TODO: Uncomment when obligations app is implemented
# class ProjectObligation(models.Model):
#     """Through model for project obligations.
#
#     Attributes:
#         project: The project associated with the obligation.
#         obligation: The obligation associated with the project.
#         created_at: The datetime when the obligation was created.
#         updated_at: The datetime when the obligation was last updated.
#
#     """
#
#     project = models.ForeignKey(
#         Project,
#         on_delete=models.CASCADE,
#         related_name="project_obligations",
#     )
#     obligation = models.ForeignKey(
#         "obligations.Obligation",
#         on_delete=models.CASCADE,
#         related_name="project_obligations",
#     )
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         unique_together = ["project", "obligation"]
#         ordering = ["project", "obligation"]
#         verbose_name = "Project Obligation"
#         verbose_name_plural = "Project Obligations"
#
#     @beartype
#     def __str__(self) -> str:
#         """Return string representation of ProjectObligation.
#
#         Returns:
#             str: The project-obligation string.
#
#         """
#         return f"{self.project.name} - {self.obligation.obligation_number}"
