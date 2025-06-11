from .models import Profile
from _typeshed import Incomplete
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete: bool
    verbose_name_plural: str

class UserAdmin(BaseUserAdmin):
    inlines: Incomplete
    list_display: Incomplete
