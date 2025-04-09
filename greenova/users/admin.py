from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    """Inline admin for user profiles."""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    """Enhanced User admin with Profile inline."""
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')


# Unregister the default User admin and register our enhanced version
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
