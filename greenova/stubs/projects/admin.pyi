from .models import Project, ProjectMembership
from _typeshed import Incomplete
from django.contrib import admin
from django.http import HttpRequest
from typing import Generic, TypeVar

logger: Incomplete
T = TypeVar('T')

class BaseModelAdmin(admin.ModelAdmin, Generic[T]):
    def dispatch(self, request: HttpRequest, object_id: str, from_field: None = None) -> T | None: ...

class ProjectMembershipInline(admin.TabularInline):
    model = ProjectMembership
    extra: int
    raw_id_fields: Incomplete

class ProjectAdmin(BaseModelAdmin[Project]):
    list_display: Incomplete
    search_fields: Incomplete
    inlines: Incomplete
    list_filter: Incomplete
    date_hierarchy: str
    def member_count(self, obj: Project) -> int: ...

class ProjectMembershipAdmin(BaseModelAdmin[ProjectMembership]):
    list_display: Incomplete
    list_filter: Incomplete
    search_fields: Incomplete
    raw_id_fields: Incomplete
    date_hierarchy: str
    ordering: Incomplete
    def get_project(self, obj: ProjectMembership) -> str: ...
    def get_user(self, obj: ProjectMembership) -> str: ...
    def get_role(self, obj: ProjectMembership) -> str: ...
    def get_created(self, obj: ProjectMembership) -> str: ...
    def save_model(self, request, obj, form, change) -> None: ...
