"""Dashboard views for Greenova environmental management application.

This module provides the main dashboard, chart, and HTMX views for
environmental obligation tracking and compliance monitoring.

"""

import logging
from datetime import datetime, timedelta  # Use timedelta from datetime
from typing import Any, TypedDict, cast  # Ensure cast is imported

from beartype import beartype  # Import beartype
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import ListView, TemplateView

# Import our new components
from obligations.constants import STATUS_IN_PROGRESS, STATUS_NOT_STARTED
from obligations.models import Obligation
from projects.models import Project

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
    last_updated: datetime  # Changed from date to datetime for consistency
    user: AbstractUser
    debug: bool
    error: str | None
    user_roles: dict[str, str]


@beartype
def get_selected_project_id(request: HttpRequest) -> str | None:
    """Return the last non-empty project_id from the query string or session.

    Args:
        request: The HttpRequest object.

    Returns:
        The selected project ID as a string, or None if not found.
    """
    project_ids: list[str] = request.GET.getlist("project_id")
    project_id_str: str | None = next(
        (pid for pid in reversed(project_ids) if pid), None
    )
    if project_id_str:
        request.session["selected_project_id"] = project_id_str
        return project_id_str

    # If project_id_str is None from GET, try to get from session
    session_value: Any = request.session.get("selected_project_id")
    # Check if session_value is a non-empty string
    if isinstance(session_value, str) and session_value:
        return session_value  # Explicitly cast to str

    # If it was stored as non-string, not found, or empty string, clear from
    # session if present
    if "selected_project_id" in request.session:
        del request.session["selected_project_id"]
    return None


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
    @beartype
    def selected_project_id(self) -> str | None:
        """Return the selected project ID from the request/session."""
        return cast(str | None, get_selected_project_id(self.request))

    @beartype
    def get_template_names(self) -> list[str]:
        """Return the template name based on request type.

        Returns:
            A list of template names.
        """
        # For any HTMX request with a target, always return the partial
        if getattr(self.request, "htmx", False):
            hx_target = self.request.headers.get("HX-Target")
            # Only return the full template if this is a top-level navigation
            # (no target or body)
            if not hx_target or hx_target == "body":
                is_dashboard = self.request.path.rstrip("/") == "/dashboard"
                is_get = self.request.method == "GET"
                if is_dashboard and is_get:
                    return [self.template_name]
            return ["dashboard/partials/dashboard_content.html"]
        return [self.template_name]

    @beartype
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests with enhanced HTMX support.

        Args:
            request: The HttpRequest object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            An HttpResponse object.
        """
        # Let the ProjectAwareDashboardMixin handle most of the logic
        response = super().get(request, *args, **kwargs)
        return response

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get the context data for template rendering.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            A dictionary containing the context data.
        """
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

            # Get overdue obligations for the overlay
            overdue_obligations = self.get_overdue_obligations()

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
                    "overdue_obligations": overdue_obligations,  # Add this line
                    "active_obligations_count": self.get_active_obligations_count(),
                    "active_obligations_trend": self.get_obligations_trend(),
                    "upcoming_deadlines_count": self.get_upcoming_deadlines_count(),
                    "active_projects_count": projects.count(),
                    "active_mechanisms_count": self.get_active_mechanisms_count(),
                    "selected_project_id": self.selected_project_id,
                }
            )
        except Exception as e:
            logger.error("Error in get_context_data: %s", e)
            context["error"] = str(e)
            context["projects"] = Project.objects.none()  # Ensure projects is empty

        return context

    @beartype
    def get_overdue_obligations(self) -> QuerySet[Obligation]:
        """Get overdue obligations for the selected project.

        Returns:
            QuerySet of overdue Obligation objects.
        """
        project_id_str: str | None = self.selected_project_id
        query_filter: dict[str, Any] = {}
        if project_id_str:
            try:
                query_filter["project_id"] = int(project_id_str)
            except ValueError:
                logger.error(
                    "Invalid project_id format '%s' for overdue obligations.",
                    project_id_str,
                )
                return cast(QuerySet[Obligation], Obligation.objects.none())

        today = timezone.now().date()
        queryset: QuerySet[Obligation] = Obligation.objects.filter(
            action_due_date__lt=today,
            status__in=[STATUS_NOT_STARTED, STATUS_IN_PROGRESS],
            **query_filter,
        ).select_related("primary_environmental_mechanism", "project")

        return queryset

    @beartype
    def get_projects(self) -> QuerySet[Project]:
        """Get projects for the current user.

        Returns:
            QuerySet[Project]: Projects for authenticated user, or empty queryset
                for anonymous users.
        """
        user = self.request.user
        # Robustly handle anonymous users (SimpleLazyObject or AnonymousUser)
        if not getattr(user, "is_authenticated", False):
            return cast(QuerySet[Project], Project.objects.none())
        try:
            # Ensure user is not AnonymousUser before filtering
            if hasattr(user, "pk"):  # Check if user has a primary key
                return cast(
                    QuerySet[Project],
                    Project.objects.filter(members=user).order_by("-created_at"),
                )
            return cast(QuerySet[Project], Project.objects.none())
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error fetching projects for user %s: %s", user, e)
            return cast(QuerySet[Project], Project.objects.none())

    @beartype
    def get_active_obligations_count(self) -> int:
        """Get count of active obligations."""
        project_id_str: str | None = self.selected_project_id
        query_filter: dict[str, Any] = {}
        if project_id_str:
            try:
                query_filter["project_id"] = int(project_id_str)
            except ValueError:
                logger.error(
                    "Invalid project_id format '%s' for active obligations count.",
                    project_id_str,
                )
                return 0  # No project selected or invalid ID

        count: int = Obligation.objects.filter(
            status__in=[STATUS_NOT_STARTED, STATUS_IN_PROGRESS], **query_filter
        ).count()
        return count

    @beartype
    def get_overdue_obligations_count(self) -> int:
        """Get count of overdue obligations for the selected project."""
        project_id_str: str | None = self.selected_project_id
        query_filter: dict[str, Any] = {}
        if project_id_str:
            try:
                query_filter["project_id"] = int(project_id_str)
            except ValueError:
                logger.error(
                    "Invalid project_id format '%s' for overdue obligations count.",
                    project_id_str,
                )
                return 0
        today = timezone.now().date()
        count: int = Obligation.objects.filter(
            action_due_date__lt=today,
            status__in=[STATUS_NOT_STARTED, STATUS_IN_PROGRESS],
            **query_filter,
        ).count()
        return count

    @beartype
    def get_obligations_trend(self) -> int:
        """Calculate the trend in obligations compared to last month.

        Returns:
            An integer representing the trend percentage.
        """
        # This would typically involve more complex time-based calculations
        # Simplified implementation for demonstration
        return 5  # Example: 5% increase

    @beartype
    def get_upcoming_deadlines_count(self) -> int:
        """Get count of upcoming deadlines in the next 7 days."""
        project_id_str: str | None = self.selected_project_id
        query_filter: dict[str, Any] = {}
        if project_id_str:
            try:
                query_filter["project_id"] = int(project_id_str)
            except ValueError:
                logger.error(
                    "Invalid project_id format '%s' for upcoming deadlines count.",
                    project_id_str,
                )
                return 0

        today = timezone.now()  # Use datetime for range comparison consistency
        seven_days_later = today + timedelta(days=7)

        count: int = Obligation.objects.filter(
            action_due_date__range=(today.date(), seven_days_later.date()),
            status__in=[STATUS_NOT_STARTED, STATUS_IN_PROGRESS],
            **query_filter,
        ).count()
        return count

    @beartype
    def get_active_mechanisms_count(self) -> int:
        """Get count of active mechanisms.

        Returns:
            An integer representing the count of active mechanisms.
        """
        # Would normally query the mechanisms model
        # Simplified placeholder implementation
        return 10  # Example count


class ChartView(ChartMixin, ProjectAwareDashboardMixin, TemplateView):
    """View for rendering charts."""

    template_name = "dashboard/partials/charts.html"

    @property
    @beartype
    def selected_project_id(self) -> str | None:
        """Return the selected project ID from the request/session.

        Returns:
            The selected project ID as a string, or None.
        """
        return cast(str | None, get_selected_project_id(self.request))

    @beartype
    def get_queryset(self) -> QuerySet[Project]:
        """Return the queryset for projects at risk of missing deadlines.

        Returns:
            A QuerySet of Project objects.
        """
        now = timezone.now()
        queryset: QuerySet[Project] = Project.objects.filter(
            obligations__action_due_date__lt=now,
            obligations__status__in=[STATUS_NOT_STARTED, STATUS_IN_PROGRESS],
        ).distinct()
        return queryset

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add projects_with_stats to the context for at-risk projects.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            A dictionary containing the context data.
        """
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        projects_with_stats = []
        # Ensure context["projects"] is iterable and contains Project instances
        projects_qs: QuerySet[Project] = context.get("projects", Project.objects.none())
        for project in projects_qs:
            overdue_obligations = project.obligations.filter(
                action_due_date__lt=now, status__in=[
                    STATUS_NOT_STARTED, STATUS_IN_PROGRESS])
            overdue_count = overdue_obligations.count()
            last_due_obligation = overdue_obligations.order_by(
                "-action_due_date"
            ).first()
            projects_with_stats.append(
                {
                    "project": project,
                    "overdue_count": overdue_count,
                    "last_due_date": last_due_obligation.action_due_date
                    if last_due_obligation
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

    @beartype
    def get_queryset(self) -> QuerySet[Project]:
        """Return projects with obligations at risk of missing deadlines.

        Returns:
            A QuerySet of Project objects, limited to 10.
        """
        now = timezone.now()
        queryset: QuerySet[Project] = Project.objects.filter(
            obligations__action_due_date__lt=now,
            obligations__status__in=[STATUS_NOT_STARTED, STATUS_IN_PROGRESS],
        ).distinct()
        return queryset[:10]

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add projects_with_stats to the context.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            A dictionary containing the context data.
        """
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        projects_with_stats = []
        # Ensure context["projects"] is iterable and contains Project instances
        projects_qs: QuerySet[Project] = context.get(
            self.context_object_name, Project.objects.none()
        )
        for project in projects_qs:  # Iterate over the resolved queryset
            overdue_obligations = project.obligations.filter(
                action_due_date__lt=now, status__in=[
                    STATUS_NOT_STARTED, STATUS_IN_PROGRESS])
            overdue_count = overdue_obligations.count()
            last_due_obligation = overdue_obligations.order_by(
                "-action_due_date"
            ).first()
            projects_with_stats.append(
                {
                    "project": project,
                    "overdue_count": overdue_count,
                    "last_due_date": last_due_obligation.action_due_date
                    if last_due_obligation
                    else None,
                }
            )
        context["projects_with_stats"] = projects_with_stats
        return context


class UpcomingObligationsView(ProjectAwareDashboardMixin, ListView):
    """View for upcoming obligations with due dates in the near future."""

    template_name = "dashboard/partials/upcoming_obligations_table.html"
    context_object_name = "obligations"

    @beartype
    def get_queryset(self) -> QuerySet[Obligation]:
        """Return obligations with due dates in the coming days.

        Filters by selected project_id if available and valid.

        Returns:
            A QuerySet of Obligation objects, limited to 10.
        """
        project_id_str = get_selected_project_id(self.request)
        if not project_id_str:
            return cast(QuerySet[Obligation], Obligation.objects.none())

        try:
            project_id_int = int(project_id_str)
        except ValueError:
            logger.error(
                "Invalid project_id format '%s' for upcoming obligations query.",
                project_id_str,
            )
            return cast(QuerySet[Obligation], Obligation.objects.none())

        today = timezone.now().date()
        future_date = today + timedelta(days=14)  # Next 14 days

        queryset: QuerySet[Obligation] = Obligation.objects.filter(
            project_id=project_id_int,
            action_due_date__gte=today,
            action_due_date__lte=future_date,
            status__in=[STATUS_NOT_STARTED, STATUS_IN_PROGRESS],
        ).order_by("action_due_date")
        return queryset[:10]

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add additional context for upcoming obligations.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            A dictionary containing the context data.
        """
        context = super().get_context_data(**kwargs)
        context["selected_project_id"] = get_selected_project_id(self.request)
        return context
