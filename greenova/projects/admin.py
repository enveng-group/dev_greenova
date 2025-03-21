from django.contrib import admin
from logging import getLogger
from typing import Optional, Sequence, TypeVar, Generic
from django.http import HttpRequest
from .models import Project, ProjectMembership

logger = getLogger(__name__)

T = TypeVar('T')

class BaseModelAdmin(admin.ModelAdmin, Generic[T]):
    """Base admin class with type safety."""

    def dispatch(self, request: HttpRequest, object_id: str, from_field: Optional[str] = None) -> Optional[T]:
        return super().get_object(request, object_id, from_field)

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

    def get_project(self, obj: ProjectMembership) -> str:
        """Get project name."""
        return str(obj.project.name)
    get_project.short_description = 'Project'
    get_project.admin_order_field = 'project__name'

    def get_user(self, obj: ProjectMembership) -> str:
        """Get username."""
        return str(obj.user.username)
    get_user.short_description = 'User'
    get_user.admin_order_field = 'user__username'

    def get_role(self, obj: ProjectMembership) -> str:
        """Get role."""
        return str(obj.role)
    get_role.short_description = 'Role'
    get_role.admin_order_field = 'role'

    def get_created(self, obj: ProjectMembership) -> str:
        """Get creation date."""
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    get_created.short_description = 'Created'
    get_created.admin_order_field = 'created_at'

    def save_model(self, request, obj, form, change):
        """Log changes when saving model."""
        action = 'updated' if change else 'created'
        logger.info(
            f'ProjectMembership {obj.id} {action} by {request.user.get_username()}'
        )
        super().save_model(request, obj, form, change)
