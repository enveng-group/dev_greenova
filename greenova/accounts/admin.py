from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import ProjectRole, User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'get_project_name',
        'get_responsibility',
    )
    list_filter = ('profile__project_name', 'groups', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'profile__project_name')

    def get_project_name(self, obj):
        return obj.profile.project_name

    get_project_name.short_description = 'Project'

    def get_responsibility(self, obj):
        return obj.profile.responsibility

    get_responsibility.short_description = 'Responsibility'


class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ('group', 'project_name', 'environmental_mechanism')
    search_fields = ('group__name', 'project_name')
    list_filter = ('project_name',)


# Unregister default User and Group
admin.site.unregister(Group)

# Register custom models
admin.site.register(User, CustomUserAdmin)
admin.site.register(ProjectRole)
admin.site.register(Group)
