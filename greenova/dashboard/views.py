"""Dashboard views for Greenova environmental management application.

This module provides the main dashboard, chart, and HTMX views for
environmental obligation tracking and compliance monitoring.
"""

import base64
import logging
from datetime import datetime, timedelta
from typing import Any, TypedDict, cast

from beartype import beartype
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import ListView, TemplateView
from django_htmx.http import push_url, trigger_client_event
from mechanisms.models import EnvironmentalMechanism
from obligations.models import Obligation
from procedures.models import Procedure
from projects.models import Project

# Import new components from PR171
try:
    from .figures import (
        create_mechanism_pie_chart_svg,
        create_obligations_status_chart_svg,
        create_procedure_pie_chart_svg,
        create_project_compliance_chart,
    )
    from .mixins import ChartMixin, ProjectAwareDashboardMixin
except ImportError:
    # Fallback if mixins don't exist yet
    ChartMixin = object
    ProjectAwareDashboardMixin = LoginRequiredMixin

    def create_obligations_status_chart_svg(project_id) -> str:
        """Fallback chart function."""
        return "<svg></svg>"

    def create_project_compliance_chart(projects):
        """Fallback chart function."""
        return None, b""

    def create_mechanism_pie_chart_svg(mechanism_id) -> str:
        """Fallback chart function."""
        return "<svg></svg>"

    def create_procedure_pie_chart_svg(procedure_id, chart_data) -> str:
        """Fallback chart function."""
        return "<svg></svg>"

# Constants for system information
SYSTEM_STATUS = "operational"  # or fetch from settings/environment
APP_VERSION = "0.0.6"  # Updated version from PR171
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


@beartype
def get_selected_project_id(request: HttpRequest) -> str | None:
    """Return the last non-empty project_id from the query string or session.

    Args:
        request: The HTTP request object.

    Returns:
        The selected project ID or None if not found.

    """
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
    request: HttpRequest
    include_charts = True  # Enable chart generation

    @property
    def selected_project_id(self) -> str | None:
        """Return the selected project ID from the request/session."""
        return get_selected_project_id(self.request)

    @beartype
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        """Initialize view setup.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        super().setup(request, *args, **kwargs)
        self.request = request

    def get_template_names(self) -> list[str]:
        """Return the template name based on request type.

        Returns:
            List of template names to use for rendering.

        """
        if getattr(self.request, "htmx", False):
            return ["dashboard/partials/dashboard_content.html"]
        return [self.template_name]

    @beartype
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests with enhanced HTMX support.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse with appropriate content and headers.

        """
        response = super().get(request, *args, **kwargs)

        # If this is an HTMX request, handle history and URL management
        if getattr(request, "htmx", False):
            # Push the URL to browser history for navigation
            current_url = request.build_absolute_uri()
            push_url(response, current_url)

            # Trigger dashboard refresh events
            trigger_client_event(response, "dashboardLoaded")

            # Also trigger project selection if project_id is in the request
            project_id = request.GET.get("project_id")
            if project_id and project_id != "0":
                logger.debug("Triggering projectSelected event with ID: %s", project_id)
                trigger_client_event(response, "projectSelected", {"id": project_id})

        return response

    @beartype
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Get the context data for template rendering.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Dictionary containing context data for template rendering.

        """
        context = super().get_context_data(**kwargs)

        try:
            user = cast("AbstractUser", self.request.user)

            # Get projects for the current user with prefetch_related
            projects = self.get_projects().prefetch_related("memberships")

            # Build user_roles dictionary
            user_roles = {}
            for project in projects:
                user_roles[str(project.pk)] = project.get_user_role(user)

            # Get selected project_id from query params
            selected_project_id = get_selected_project_id(self.request)

            context.update({
                "projects": projects,
                "selected_project_id": selected_project_id,
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
                "upcoming_7_count": self.get_upcoming_count(7),
                "upcoming_14_count": self.get_upcoming_count(14),
                "upcoming_30_count": self.get_upcoming_count(30),
                "upcoming_90_count": self.get_upcoming_count(90),
            })

            # Add chart data
            self.add_specific_charts(context)

            # Add a flag to check if project selector should exist
            context["project_selector_exists"] = self.get_projects().exists()

            logger.debug(
                "Dashboard context: selected_project_id=%s",
                selected_project_id,
            )

        except (AttributeError, ValueError) as e:
            logger.exception("Error in dashboard context: %s", e)
            context["error"] = str(e)

        # Add chart generation
        try:
            _, compliance_chart = create_project_compliance_chart(context["projects"])
            context["compliance_chart"] = base64.b64encode(compliance_chart).decode(
                "utf-8",
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

    @beartype
    def add_specific_charts(self, context: dict[str, Any]) -> None:
        """Add view-specific chart data to the context.

        Args:
            context: The context dictionary to update.

        """
        # Add any dashboard-specific chart data here
        # This method is intentionally left minimal as the base charts
        # are already being added in the get_context_data method

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
            return Project.objects.none()
        try:
            return Project.objects.filter(members=user).order_by("-created_at")
        except Exception as e:
            logger.exception("Error fetching projects for user %s: %s", user, e)
            return Project.objects.none()

    @beartype
    def get_active_obligations_count(self) -> int:
        """Get count of active obligations.

        Returns:
            Count of active obligations for the selected project.

        """
        project_id = self.selected_project_id
        query_filter = {}
        if project_id:
            query_filter["project_id"] = project_id

        return Obligation.objects.filter(
            status__in=["pending", "in_progress"], **query_filter,
        ).count()

    @beartype
    def get_overdue_obligations_count(self) -> int:
        """Get count of overdue obligations for the selected project.

        Returns:
            Count of overdue obligations.

        """
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

    @beartype
    def get_obligations_trend(self) -> int:
        """Calculate the trend in obligations compared to last month.

        Returns:
            Percentage change in obligations (simplified implementation).

        """
        # This would typically involve more complex time-based calculations
        # Simplified implementation for demonstration
        return 5  # Example: 5% increase

    @beartype
    def get_upcoming_deadlines_count(self) -> int:
        """Get count of upcoming deadlines in the next 7 days.

        Returns:
            Count of upcoming deadlines.

        """
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

    @beartype
    def get_active_mechanisms_count(self) -> int:
        """Get count of active mechanisms.

        Returns:
            Count of active mechanisms (placeholder implementation).

        """
        # Would normally query the mechanisms model
        # Simplified placeholder implementation
        return 10  # Example count

    @beartype
    def get_upcoming_count(self, days: int) -> int:
        """Get count of obligations due in the next N days for the selected project."""
        project_id = self.selected_project_id
        query_filter = {}
        if project_id:
            query_filter["project_id"] = project_id
        today = timezone.now().date()
        future_date = today + timedelta(days=days)
        return Obligation.objects.filter(
            action_due_date__gte=today,
            action_due_date__lte=future_date,
            status__in=["pending", "in_progress"],
            **query_filter,
        ).count()


class ChartView(ChartMixin, ProjectAwareDashboardMixin, TemplateView):
    """View for rendering charts."""

    template_name = "dashboard/partials/charts.html"

    @property
    def selected_project_id(self) -> str | None:
        """Return the selected project ID from the request/session."""
        return get_selected_project_id(self.request)

    def get_queryset(self) -> QuerySet[Project]:
        """Return the queryset for projects at risk of missing deadlines.

        Returns:
            QuerySet of projects with overdue obligations.

        """
        now = timezone.now()
        return Project.objects.filter(
            obligations__action_due_date__lt=now,
            obligations__status__in=["pending", "in_progress"],
        ).distinct()

    @beartype
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add projects_with_stats to the context for at-risk projects.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Context dictionary with project statistics.

        """
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        projects_with_stats = []
        for project in context["projects"]:
            overdue_obligations = project.obligations.filter(
                action_due_date__lt=now, status__in=["pending", "in_progress"],
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
                },
            )
        context["projects_with_stats"] = projects_with_stats
        return context


class ProjectsAtRiskView(ProjectAwareDashboardMixin, ListView):
    """HTMX view for projects at risk of missing deadlines."""

    model = Project
    template_name = "dashboard/partials/projects_at_risk_table.html"
    context_object_name = "projects"

    def get_queryset(self) -> QuerySet[Project]:
        """Return projects with obligations at risk of missing deadlines.

        Returns:
            QuerySet of projects with overdue obligations (limited to 10).

        """
        now = timezone.now()
        queryset = Project.objects.filter(
            obligations__action_due_date__lt=now,
            obligations__status__in=["pending", "in_progress"],
        ).distinct()
        return queryset[:10]

    @beartype
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add projects_with_stats to the context.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Context dictionary with project statistics.

        """
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        projects_with_stats = []
        for project in context["projects"]:
            overdue_obligations = project.obligations.filter(
                action_due_date__lt=now, status__in=["pending", "in_progress"],
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
                },
            )
        context["projects_with_stats"] = projects_with_stats
        return context


class UpcomingObligationsView(ProjectAwareDashboardMixin, ListView):
    """View for upcoming obligations with due dates in the near future."""

    template_name = "dashboard/partials/upcoming_obligations_table.html"
    context_object_name = "obligations"

    def get_queryset(self) -> QuerySet[Obligation]:
        """Return obligations with due dates in the coming days.

        Returns:
            QuerySet of upcoming obligations for the selected project.

        """
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

    @beartype
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add additional context for upcoming obligations.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Context dictionary with selected project information.

        """
        context = super().get_context_data(**kwargs)
        context["selected_project_id"] = get_selected_project_id(self.request)
        return context


# Drilldown views for Issue #165
@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class MechanismDrilldownView(LoginRequiredMixin, TemplateView):
    """View for mechanism drilldown charts in the obligation workflow."""

    template_name = "dashboard/partials/mechanism_drilldown.html"
    login_url = "account_login"

    @beartype
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Get context data for mechanism drilldown charts.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Context dictionary with mechanism chart data.

        """
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get("project_id")

        if not project_id or project_id == "0":
            context["error"] = "No project selected"
            return context

        try:
            project = get_object_or_404(Project, id=project_id)
            mechanisms = EnvironmentalMechanism.objects.filter(project=project)

            # Generate mechanism charts data
            mechanism_charts = []
            for mechanism in mechanisms:
                # Create SVG chart for each mechanism
                chart_svg = create_mechanism_pie_chart_svg(mechanism.id)
                mechanism_charts.append({
                    "id": mechanism.id,
                    "name": mechanism.name,
                    "chart_svg": chart_svg,
                    "total_obligations": (
                        mechanism.not_started_count +
                        mechanism.in_progress_count +
                        mechanism.completed_count +
                        mechanism.overdue_count
                    ),
                    "overdue_count": mechanism.overdue_count,
                })

            context.update({
                "project": project,
                "mechanisms": mechanisms,
                "mechanism_charts": mechanism_charts,
                "selected_project_id": project_id,
            })

        except (Project.DoesNotExist, ValueError) as e:
            logger.exception("Error in mechanism drilldown: %s", e)
            context["error"] = f"Project not found or invalid ID: {project_id}"

        return context


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ProcedureDrilldownView(LoginRequiredMixin, TemplateView):
    """View for procedure drilldown charts in the obligation workflow."""

    template_name = "dashboard/partials/procedure_drilldown.html"
    login_url = "account_login"

    @beartype
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Get context data for procedure drilldown charts.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Context dictionary with procedure chart data.

        """
        context = super().get_context_data(**kwargs)
        mechanism_id = self.request.GET.get("mechanism_id")
        project_id = self.request.GET.get("project_id")

        if not mechanism_id:
            context["error"] = "No mechanism selected"
            return context

        try:
            mechanism = get_object_or_404(EnvironmentalMechanism, id=mechanism_id)
            procedures = Procedure.objects.filter(mechanism=mechanism)

            # Generate procedure charts data
            procedure_charts = []
            for procedure in procedures:
                # Get obligations for this procedure
                obligations = Obligation.objects.filter(procedure=procedure)

                # Calculate status counts
                not_started = obligations.filter(status="not_started").count()
                in_progress = obligations.filter(status="in_progress").count()
                completed = obligations.filter(status="completed").count()
                overdue = sum(1 for obj in obligations if obj.is_overdue)

                # Create chart data
                chart_data = {
                    "not_started": not_started,
                    "in_progress": in_progress,
                    "completed": completed,
                    "overdue": overdue,
                }

                # Create SVG chart for this procedure
                chart_svg = create_procedure_pie_chart_svg(procedure.id, chart_data)

                procedure_charts.append({
                    "id": procedure.id,
                    "name": procedure.name,
                    "chart_svg": chart_svg,
                    "chart_data": chart_data,
                    "total_obligations": not_started + in_progress + completed + overdue,
                    "overdue_count": overdue,
                })

            context.update({
                "mechanism": mechanism,
                "procedures": procedures,
                "procedure_charts": procedure_charts,
                "selected_project_id": project_id,
                "selected_mechanism_id": mechanism_id,
            })

        except (EnvironmentalMechanism.DoesNotExist, ValueError) as e:
            logger.exception("Error in procedure drilldown: %s", e)
            context["error"] = f"Mechanism not found or invalid ID: {mechanism_id}"

        return context


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ObligationListDrilldownView(LoginRequiredMixin, ListView):
    """View for final obligation list in the drilldown workflow."""

    model = Obligation
    template_name = "dashboard/partials/obligation_list_drilldown.html"
    context_object_name = "obligations"
    paginate_by = 20
    login_url = "account_login"

    @beartype
    def get_queryset(self) -> QuerySet[Obligation]:
        """Get obligations filtered by procedure.

        Returns:
            QuerySet of obligations for the selected procedure.

        """
        procedure_id = self.request.GET.get("procedure_id")
        mechanism_id = self.request.GET.get("mechanism_id")
        project_id = self.request.GET.get("project_id")

        queryset = Obligation.objects.select_related(
            "project", "mechanism", "procedure",
        ).prefetch_related("attachments")

        # Filter by procedure if provided
        if procedure_id:
            queryset = queryset.filter(procedure_id=procedure_id)
        elif mechanism_id:
            queryset = queryset.filter(mechanism_id=mechanism_id)
        elif project_id:
            queryset = queryset.filter(project_id=project_id)
        else:
            queryset = queryset.none()

        # Order by overdue status first, then by due date
        return queryset.extra(
            select={
                "is_overdue_calc": """
                    CASE WHEN action_due_date < %s AND status IN ('not_started', 'in_progress')
                    THEN 1 ELSE 0 END
                """,
            },
            select_params=[timezone.now().date()],
        ).order_by("-is_overdue_calc", "action_due_date")

    @beartype
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add additional context for obligation list.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Context dictionary with drilldown navigation data.

        """
        context = super().get_context_data(**kwargs)

        procedure_id = self.request.GET.get("procedure_id")
        mechanism_id = self.request.GET.get("mechanism_id")
        project_id = self.request.GET.get("project_id")

        # Add breadcrumb context
        breadcrumbs = []
        if project_id:
            try:
                project = get_object_or_404(Project, id=project_id)
                breadcrumbs.append({"name": project.name, "type": "project"})
            except Project.DoesNotExist:
                pass

        if mechanism_id:
            try:
                mechanism = get_object_or_404(EnvironmentalMechanism, id=mechanism_id)
                breadcrumbs.append({"name": mechanism.name, "type": "mechanism"})
            except EnvironmentalMechanism.DoesNotExist:
                pass

        if procedure_id:
            try:
                procedure = get_object_or_404(Procedure, id=procedure_id)
                breadcrumbs.append({"name": procedure.name, "type": "procedure"})
            except Procedure.DoesNotExist:
                pass

        # Calculate counts for display
        obligations = context["obligations"]
        overdue_count = sum(1 for obj in obligations if obj.is_overdue)
        active_count = obligations.filter(status="in_progress").count()

        context.update({
            "breadcrumbs": breadcrumbs,
            "selected_project_id": project_id,
            "selected_mechanism_id": mechanism_id,
            "selected_procedure_id": procedure_id,
            "overdue_count": overdue_count,
            "active_count": active_count,
            "total_count": obligations.count(),
        })

        return context
