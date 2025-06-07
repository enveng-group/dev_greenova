from _typeshed import Incomplete
from beartype import beartype
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
    EnvironmentalObligationForm,
    UserProfileForm,
)
from .models import AuditLog

class EnvironmentalObligationAdmin(admin.ModelAdmin):
    form = EnvironmentalObligationForm
    search_fields: Incomplete
    list_display: Incomplete
    list_filter: Incomplete

class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display: Incomplete
    search_fields: Incomplete
    list_filter: Incomplete
    ordering: Incomplete

class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm
    list_display: Incomplete
    search_fields: Incomplete
    ordering: Incomplete

class AuditLogAdmin(admin.ModelAdmin):
    list_display: Incomplete
    search_fields: Incomplete
    list_filter: Incomplete
    ordering: Incomplete
    readonly_fields: Incomplete
    @beartype
    def get_queryset(self, request: HttpRequest) -> QuerySet[AuditLog]: ...
