from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from django.forms import ModelForm
from logging import getLogger
from .models import Project, ProjectMembership
from obligations.models import Obligation

logger = getLogger(__name__)

class ProjectMembershipInline(admin.TabularInline):
    """Inline admin for project memberships."""
    model = ProjectMembership
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin configuration for Project model."""
    list_display = ('id', 'name', 'member_count')
    search_fields = ('name',)
    inlines = [ProjectMembershipInline]

    def member_count(self, obj: Project) -> int:
        """Get number of project members."""
        return obj.members.count()
    member_count.short_description = 'Members'

    def save_model(self, request: HttpRequest, obj: Project, form: ModelForm, change: bool) -> None:
        try:
            logger.info(f"Admin saving project: {obj.name}")
            super().save_model(request, obj, form, change)
        except Exception as e:
            logger.error(f"Admin save error: {str(e)}")
            raise

@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    """Admin configuration for ProjectMembership model."""
    list_display = ('user', 'project', 'role', 'created_at')
    list_filter = ('role', 'project')
    search_fields = ('user__username', 'project__name')
    raw_id_fields = ('user', 'project')