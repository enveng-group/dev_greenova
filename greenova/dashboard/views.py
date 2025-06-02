"""Dashboard views for Greenova environmental management application.

This module provides the main dashboard, chart, and HTMX views for
environmental obligation tracking and compliance monitoring.

"""

import base64
import logging
from datetime import datetime, timedelta  # Use timedelta from datetime
from typing import Any, TypedDict, cast

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import ListView, TemplateView
from obligations.models import Obligation
from projects.models import Project

# Import our new components
from .figures import (
    create_obligations_status_chart_svg,
    create_project_compliance_chart,
)
from .mixins import ChartMixin, ProjectAwareDashboardMixin

# Constants for system information
SYSTEM_STATUS = "operational"  # or fetch from settings/environment
APP_VERSION = "0.0.6"  # or fetch from settings/environment
LAST_UPDATED = datetime.now().date()  # or fetch from settings/environment

logger = logging.getLogger(__name__)


class DashboardContext(TypedDict):
    """Type definition for dashboard context data."""

    projects: QuerySet[Project]
    selected_project_id: str | None
    system_status: str
    app_version: str
    last_updated: datetime
    user: AbstractUser
    debug: bool
    error: str | None
    user_roles: dict[str, str]


def get_selected_project_id(request: HttpRequest) -> int | None:
    """Return the last non-empty project_id from the query string or session."""
    project_ids = request.GET.getlist("project_id")
    project_id = next((pid for pid in reversed(project_ids) if pid), None)
    if project_id:
        request.session["selected_project_id"] = project_id
    elif "selected_project_id" in request.session:
        del request.session["selected_project_id"]
    return project_id or request.session.get("selected_project_id")


@method_decorator(cache_control(max_age=60), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class DashboardHomeView(ProjectAwareDashboardMixin, TemplateView):
    """Main dashboard view."""

    template_name = "dashboard/dashboard.html"
    login_url = "account_login"
    redirect_field_name = "next"
    request: HttpRequest  # Ensure this matches the base class type
    include_charts = True  # Enable chart generation

    @property
    def selected_project_id(self) -> str | None:
        """Return the selected project ID from the request/session."""
        return get_selected_project_id(self.request)

    def get_template_names(self):
        """Return the template name based on request type."""
        if getattr(self.request, "htmx", False):
            return ["dashboard/partials/dashboard_content.html"]
        return [self.template_name]

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests with enhanced HTMX support."""
        # Let the ProjectAwareDashboardMixin handle most of the logic
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Get the context data for template rendering."""
        # Let the mixin handle project selection
        context = super().get_context_data(**kwargs)

        try:
            user = cast(AbstractUser, self.request.user)

            # Get projects for the current user with prefetch_related
            projects = self.get_projects().prefetch_related("memberships")

            # Build user_roles dictionary
            user_roles = {}
            for project in projects:
                user_roles[str(project.pk)] = project.get_user_role(user)

            # Get dashboard statistics
            context.update(
                {
                    "projects": projects,
                    "system_status": SYSTEM_STATUS,
                    "app_version": APP_VERSION,
                    "last_updated": LAST_UPDATED,
                    "user": user,
                    "debug": settings.DEBUG,
                    "error": None,
                    "user_roles": user_roles,
                    "show_feedback_link": True,
                    "overdue_obligations_count": self.get_overdue_obligations_count(),
                    "active_obligations_count": self.get_active_obligations_count(),
                    "active_obligations_trend": self.get_obligations_trend(),
                    "upcoming_deadlines_count": self.get_upcoming_deadlines_count(),
                    "active_projects_count": projects.count(),
                    "active_mechanisms_count": self.get_active_mechanisms_count(),
                    "selected_project_id": get_selected_project_id(self.request),
                }
            )

            # Add chart data - this is handled by the ChartMixin parent class
            # but we can add additional charts specific to this view
            self.add_specific_charts(context)

            # Add a flag to check if project selector should exist
            context["project_selector_exists"] = self.get_projects().exists()

        except (AttributeError, ValueError) as e:
            logger.exception("Error in dashboard context: %s", e)
            context["error"] = str(e)

        try:
            _, compliance_chart = create_project_compliance_chart(context["projects"])
            context["compliance_chart"] = base64.b64encode(compliance_chart).decode(
                "utf-8"
            )
        except Exception as exc:
            logger.exception("Error generating compliance chart: %s", exc)

        try:
            selected_project_id = context.get("selected_project_id")
            context["obligations_status_chart_svg"] = (
                create_obligations_status_chart_svg(selected_project_id)
            )
        except Exception as exc:
            logger.exception("Error generating obligations status chart: %s", exc)

        return context

    def add_specific_charts(self, context: dict[str, Any]) -> None:
        """
        Add view-specific chart data to the context.

        Args:
            context: The context dictionary to update
        """
        # Add any dashboard-specific chart data here
        # This method is intentionally left minimal as the base charts
        # are already being added in the get_context_data method

    def get_projects(self) -> QuerySet[Project]:
        """Get projects for the current user.

        Returns:
            QuerySet[Project]: Projects for authenticated user, or empty queryset
                for anonymous users.
        """
        user = self.request.user
        # Robustly handle anonymous users (SimpleLazyObject or AnonymousUser)
        if not getattr(user, "is_authenticated", False):
            return Project.objects.none()
        try:
            return Project.objects.filter(members=user).order_by("-created_at")
        except Exception as e:
            logger.error("Error fetching projects for user %s: %s", user, e)
            return Project.objects.none()

    def get_active_obligations_count(self) -> int:
        """Get count of active obligations."""
        project_id = self.selected_project_id
        query_filter = {}
        if project_id:
            query_filter["project_id"] = project_id

        return Obligation.objects.filter(
            status__in=["pending", "in_progress"], **query_filter
        ).count()

    def get_overdue_obligations_count(self) -> int:
        """Get count of overdue obligations for the selected project."""
        project_id = self.selected_project_id
        query_filter = {}
        if project_id:
            query_filter["project_id"] = project_id
        today = timezone.now().date()
        return Obligation.objects.filter(
            action_due_date__lt=today,
            status__in=["pending", "in_progress"],
            **query_filter,
        ).count()

    def get_obligations_trend(self) -> int:
        """Calculate the trend in obligations compared to last month."""
        # This would typically involve more complex time-based calculations
        # Simplified implementation for demonstration
        return 5  # Example: 5% increase

    def get_upcoming_deadlines_count(self) -> int:
        """Get count of upcoming deadlines in the next 7 days."""
        project_id = self.selected_project_id
        query_filter = {}
        if project_id:
            query_filter["project_id"] = project_id

        today = timezone.now()
        seven_days_later = today + timedelta(days=7)

        return Obligation.objects.filter(
            action_due_date__range=(today, seven_days_later),
            status__in=["pending", "in_progress"],
            **query_filter,
        ).count()

    def get_active_mechanisms_count(self) -> int:
        """Get count of active mechanisms."""
        # Would normally query the mechanisms model
        # Simplified placeholder implementation
        return 10  # Example count


class ChartView(ChartMixin, ProjectAwareDashboardMixin, TemplateView):
    """View for rendering charts."""

    template_name = "dashboard/partials/charts.html"

    @property
    def selected_project_id(self) -> str | None:
        """Return the selected project ID from the request/session."""
        return get_selected_project_id(self.request)

    def get_queryset(self):
        """Return the queryset for projects at risk of missing deadlines."""
        now = timezone.now()
        queryset = Project.objects.filter(
            obligations__action_due_date__lt=now,
            obligations__status__in=["pending", "in_progress"],
        ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        """Add projects_with_stats to the context for at-risk projects."""
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        projects_with_stats = []
        for project in context["projects"]:
            overdue_obligations = project.obligations.filter(
                action_due_date__lt=now, status__in=["pending", "in_progress"]
            )
            overdue_count = overdue_obligations.count()
            last_due_date = overdue_obligations.order_by("-action_due_date").first()
            projects_with_stats.append(
                {
                    "project": project,
                    "overdue_count": overdue_count,
                    "last_due_date": last_due_date.action_due_date
                    if last_due_date
                    else None,
                }
            )
        context["projects_with_stats"] = projects_with_stats
        return context


class ProjectsAtRiskView(ProjectAwareDashboardMixin, ListView):
    """HTMX view for projects at risk of missing deadlines."""

    model = Project
    template_name = "dashboard/partials/projects_at_risk_table.html"
    context_object_name = "projects"

    def get_queryset(self):
        """Return projects with obligations at risk of missing deadlines."""
        now = timezone.now()
        queryset = Project.objects.filter(
            obligations__action_due_date__lt=now,
            obligations__status__in=["pending", "in_progress"],
        ).distinct()
        return queryset[:10]

    def get_context_data(self, **kwargs):
        """Add projects_with_stats to the context."""
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        projects_with_stats = []
        for project in context["projects"]:
            overdue_obligations = project.obligations.filter(
                action_due_date__lt=now, status__in=["pending", "in_progress"]
            )
            overdue_count = overdue_obligations.count()
            last_due_date = overdue_obligations.order_by("-action_due_date").first()
            projects_with_stats.append(
                {
                    "project": project,
                    "overdue_count": overdue_count,
                    "last_due_date": last_due_date.action_due_date
                    if last_due_date
                    else None,
                }
            )
        context["projects_with_stats"] = projects_with_stats
        return context


class UpcomingObligationsView(ProjectAwareDashboardMixin, ListView):
    """View for upcoming obligations with due dates in the near future."""

    template_name = "dashboard/partials/upcoming_obligations_table.html"
    context_object_name = "obligations"

    def get_queryset(self):
        """Return obligations with due dates in the coming days."""
        project_id = get_selected_project_id(self.request)
        if not project_id:
            return Obligation.objects.none()

        today = timezone.now().date()
        future_date = today + timedelta(days=14)  # Next 14 days

        return Obligation.objects.filter(
            project_id=project_id,
            action_due_date__gte=today,
            action_due_date__lte=future_date,
            status__in=["pending", "in_progress"],
        ).order_by("action_due_date")[:10]

    def get_context_data(self, **kwargs):
        """Add additional context for upcoming obligations."""
        context = super().get_context_data(**kwargs)
        context["selected_project_id"] = get_selected_project_id(self.request)
        return context
