from logging import getLogger
from typing import Generic, Optional, TypeVar

from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest

from .models import Project, ProjectMembership

logger = getLogger(__name__)

T = TypeVar('T')

class BaseModelAdmin(admin.ModelAdmin, Generic[T]):
    """Base admin class with type safety."""

<<<<<<< HEAD
    def dispatch(
        self, request: HttpRequest, object_id: str, from_field: None = None
    ) -> Optional[T]:
        obj = super().get_object(request, object_id, from_field)
        if obj:
            if not self.has_view_or_change_permission(request, obj):
                logger.warning(
                    'Permission denied for user %s on object %s',
                    request.user,
                    object_id
                )
                raise PermissionDenied(
                    'You do not have permission to access this object.'
                )
        return obj
=======
    def dispatch(self, request: HttpRequest, object_id: str, from_field: Optional[str] = None) -> Optional[T]:
        return super().get_object(request, object_id, from_field)
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

class ProjectMembershipInline(admin.TabularInline):
    """Inline admin for project memberships."""
    model = ProjectMembership
    extra = 1
    raw_id_fields = ('user',)

@admin.register(Project)
class ProjectAdmin(BaseModelAdmin[Project]):
    """Admin configuration for Project model."""
    list_display = ('id', 'name', 'member_count', 'created_at')
    search_fields = ('name',)
    inlines = [ProjectMembershipInline]
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'

    @admin.display(description='Members')
    def member_count(self, obj: Project) -> int:
        """Get number of project members."""
        return obj.get_member_count()

@admin.register(ProjectMembership)
class ProjectMembershipAdmin(BaseModelAdmin[ProjectMembership]):
    """Admin configuration for ProjectMembership model."""
    list_display = ('id', 'get_project', 'get_user', 'get_role', 'get_created')
    list_filter = ('project', 'role', 'created_at')
    search_fields = ('user__username', 'project__name')
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    @admin.display(
        description='Project',
        ordering='project__name',
    )
    def get_project(self, obj: ProjectMembership) -> str:
        """Get project name."""
        return str(obj.project.name)

    @admin.display(
        description='User',
        ordering='user__username',
    )
    def get_user(self, obj: ProjectMembership) -> str:
        """Get username."""
        return str(obj.user.username)

    @admin.display(
        description='Role',
        ordering='role',
    )
    def get_role(self, obj: ProjectMembership) -> str:
        """Get role."""
        return str(obj.role)

    @admin.display(
        description='Created',
        ordering='created_at',
    )
    def get_created(self, obj: ProjectMembership) -> str:
        """Get creation date."""
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

    def save_model(self, request, obj, form, change):
        """Log changes when saving model."""
        action = 'updated' if change else 'created'
        logger.info(
            'ProjectMembership %s %s by %s',
            obj.id, action, request.user.get_username()
        )
        super().save_model(request, obj, form, change)
