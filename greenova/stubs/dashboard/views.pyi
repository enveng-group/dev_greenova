from .mixins import ChartMixin, ProjectAwareDashboardMixin
from _typeshed import Incomplete
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_GET as require_GET
from django.views.generic import ListView, TemplateView
from projects.models import Project
from typing import Any, TypedDict

SYSTEM_STATUS: str
APP_VERSION: str
LAST_UPDATED: Incomplete
logger: Incomplete

class DashboardContext(TypedDict):
    projects: QuerySet[Project]
    selected_project_id: str | None
    system_status: str
    app_version: str
    last_updated: datetime
    user: AbstractUser
    debug: bool
    error: str | None
    user_roles: dict[str, str]

def get_selected_project_id(request: HttpRequest) -> int | None: ...

class DashboardHomeView(ProjectAwareDashboardMixin, TemplateView):
    template_name: str
    login_url: str
    redirect_field_name: str
    request: HttpRequest
    include_charts: bool
    @property
    def selected_project_id(self) -> str | None: ...
    def get_template_names(self): ...
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]: ...
    def add_specific_charts(self, context: dict[str, Any]) -> None: ...
    def get_projects(self) -> QuerySet[Project]: ...
    def get_active_obligations_count(self) -> int: ...
    def get_overdue_obligations_count(self) -> int: ...
    def get_obligations_trend(self) -> int: ...
    def get_upcoming_deadlines_count(self, days: int) -> int: ...
    def get_active_mechanisms_count(self) -> int: ...

class ChartView(ChartMixin, ProjectAwareDashboardMixin, TemplateView):
    template_name: str
    @property
    def selected_project_id(self) -> str | None: ...
    def get_queryset(self): ...
    def get_context_data(self, **kwargs): ...

class ProjectsAtRiskView(ProjectAwareDashboardMixin, ListView):
    model = Project
    template_name: str
    context_object_name: str
    def get_queryset(self): ...
    def get_context_data(self, **kwargs): ...

def search_obligations(request): ...

class OverdueObligationsView(ProjectAwareDashboardMixin, ListView):
    template_name: str
    context_object_name: str
    def get_queryset(self): ...
    def get_context_data(self, **kwargs): ...

class ActiveObligationsView(ProjectAwareDashboardMixin, ListView):
    template_name: str
    context_object_name: str
    def get_queryset(self): ...
    def get_context_data(self, **kwargs): ...

class UpcomingObligationsDaysView(ProjectAwareDashboardMixin, ListView):
    template_name: str
    context_object_name: str
    def get_days(self): ...
    def get_queryset(self): ...

class UpcomingObligationsView(ProjectAwareDashboardMixin, ListView):
    template_name: str
    context_object_name: str
    def get_queryset(self): ...
    def get_context_data(self, **kwargs): ...
