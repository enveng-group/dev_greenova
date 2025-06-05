"""Admin configuration for the projects app.

This module provides admin classes for the Project and ProjectMembership models,
including permission checks, inline admin, and logging.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from logging import getLogger
from typing import TypeVar, Any

from beartype import beartype
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest

from .models import Project, ProjectMembership
from .permissions import user_can_view_project

logger = getLogger(__name__)

T = TypeVar("T")


class BaseModelAdmin[T](admin.ModelAdmin):
    """Base admin class with type safety and permission checks."""

    @beartype
    def dispatch(
        self, request: HttpRequest, object_id: str, from_field: None = None,
    ) -> T | None:
        """Get object with type safety and permission checking.

        Args:
            request: The HTTP request object.
            object_id: The object's primary key or unique identifier.
            from_field: The field to use for lookup (optional).

        Returns:
            The model instance if found and permitted, otherwise None.

        Raises:
            PermissionDenied: If the user does not have permission to view the object.
        """
        obj = super().get_object(request, object_id, from_field)
        if obj and not user_can_view_project(request.user, obj):
            logger.warning(
                "Permission denied for user %s on object %s",
                request.user,
                object_id,
            )
            msg = "You do not have permission to access this object."
            raise PermissionDenied(msg)
        return obj


class ProjectMembershipInline(admin.TabularInline):
    """Inline admin for project memberships."""

    model = ProjectMembership
    extra = 1
    raw_id_fields = ("user",)


@admin.register(Project)
class ProjectAdmin(BaseModelAdmin[Project]):
    """Admin configuration for Project model."""

    list_display = ("id", "name", "member_count", "created_at")
    search_fields = ("name",)
    inlines = [ProjectMembershipInline]
    list_filter = ("created_at",)
    date_hierarchy = "created_at"

    @admin.display(description="Members")
    @beartype
    def member_count(self, obj: Project) -> int:
        """Get number of project members.

        Args:
            obj: The Project instance.

        Returns:
            The number of members in the project.
        """
        return obj.get_member_count()


@admin.register(ProjectMembership)
class ProjectMembershipAdmin(BaseModelAdmin[ProjectMembership]):
    """Admin configuration for ProjectMembership model."""

    list_display = ("id", "get_project", "get_user", "get_role", "get_created")
    list_filter = ("project", "role", "created_at")
    search_fields = ("user__username", "project__name")
    raw_id_fields = ("user",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    @admin.display(
        description="Project",
        ordering="project__name",
    )
    @beartype
    def get_project(self, obj: ProjectMembership) -> str:
        """Get project name.

        Args:
            obj: The ProjectMembership instance.

        Returns:
            The name of the project.
        """
        return str(obj.project.name)

    @admin.display(
        description="User",
        ordering="user__username",
    )
    @beartype
    def get_user(self, obj: ProjectMembership) -> str:
        """Get username.

        Args:
            obj: The ProjectMembership instance.

        Returns:
            The username of the user.
        """
        return str(obj.user.username)

    @admin.display(
        description="Role",
        ordering="role",
    )
    @beartype
    def get_role(self, obj: ProjectMembership) -> str:
        """Get role.

        Args:
            obj: The ProjectMembership instance.

        Returns:
            The role of the user in the project.
        """
        return str(obj.role)

    @admin.display(
        description="Created",
        ordering="created_at",
    )
    @beartype
    def get_created(self, obj: ProjectMembership) -> str:
        """Get creation date.

        Args:
            obj: The ProjectMembership instance.

        Returns:
            The creation date as a formatted string.
        """
        return obj.created_at.strftime("%Y-%m-%d %H:%M")

    @beartype
    def save_model(
        self, request: HttpRequest, obj: ProjectMembership, form: Any, change: bool
    ) -> None:
        """Log changes when saving model.

        Args:
            request: The HTTP request object.
            obj: The ProjectMembership instance being saved.
            form: The model form instance.
            change: Boolean indicating if this is an update.

        Returns:
            None.
        """
        action = "updated" if change else "created"
        logger.info(
            "ProjectMembership %s %s by %s",
            obj.id, action, request.user.get_username(),
        )
        super().save_model(request, obj, form, change)
