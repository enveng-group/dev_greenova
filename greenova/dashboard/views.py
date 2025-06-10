"""Copyright (C) 2024 Adrian Gallo <agallo@enveng-group.com.au>
This file is part of Greenova and is licensed under the AGPL-3.0.

Dashboard app views for Greenova.
"""

import logging
from typing import Any

from beartype import beartype
from dashboard.utils import sanitize_html  # noqa: F401
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView

from .models import ComplianceMetrics, DashboardData, ObligationSummary, ProjectSummary

logger = logging.getLogger(__name__)


@beartype
class DashboardIndexView(LoginRequiredMixin, TemplateView):
    """Main dashboard view for authenticated users.

    Aggregates project summaries, obligation summaries, and compliance metrics
    for the current user and passes them to the dashboard template.
    """

    template_name = "dashboard/dashboard_home.html"

    @beartype
    def dispatch(
        self, request: HttpRequest, *args: object, **kwargs: object
    ) -> HttpResponse:
        if not request.user.is_authenticated:
            return render(
                request,
                "dashboard/dashboard_unauthenticated.html",
                {"login_message": "Please log in to access the dashboard"},
                status=200,
            )
        return super().dispatch(request, *args, **kwargs)

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data for the dashboard template.

        Args:
            **kwargs: Additional context variables.

        Returns:
            Context dictionary for the dashboard template.

        """
        context = super().get_context_data(**kwargs)
        self.request.user
        # Aggregate dashboard data for the current user
        # (Replace with real user/project scoping as needed)
        project_summaries = ProjectSummary.objects.all()
        obligation_summaries = ObligationSummary.objects.all()
        compliance_metrics = ComplianceMetrics.objects.first()
        dashboard_data = DashboardData.objects.first()
        context.update(
            {
                "project_summaries": project_summaries,
                "obligation_summaries": obligation_summaries,
                "compliance_metrics": compliance_metrics,
                "dashboard_data": dashboard_data,
                "user_projects": project_summaries,  # for project selector partial
            }
        )
        return context


@beartype
class DashboardUnauthenticatedView(TemplateView):
    """Dashboard view for unauthenticated users: shows login prompt."""

    template_name = "dashboard/dashboard_unauthenticated.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["login_message"] = "Please log in to access the dashboard"
        return context


@beartype
class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Main dashboard view with permissions and CSP support.

    Requires user to be authenticated and have 'dashboard.view_dashboard' perm.
    Integrates django-guardian for object-level permissions (future-ready).
    Sets Content Security Policy headers for enhanced security.
    """

    permission_required = "dashboard.view_dashboard"
    raise_exception = True

    @method_decorator(ensure_csrf_cookie)
    @beartype
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Render the dashboard page with CSP headers and permission checks.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments (unused).
            **kwargs: Additional keyword arguments (unused).

        Returns:
            HttpResponse: The rendered dashboard page.

        """
        response = self.render_to_response({})
        # Set/override CSP headers for dashboard if needed
        response["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self' 'unsafe-inline'; "
            "script-src 'self'; img-src 'self' data:;"
        )
        logger.info("Dashboard page rendered for user %s", request.user.pk)
        return response

    def render_to_response(self, context: dict[str, Any]) -> HttpResponse:
        """Render the dashboard template with context.

        Args:
            context: Context data for the template.

        Returns:
            HttpResponse: The rendered template response.

        """
        return render(self.request, "dashboard/dashboard.html", context)


@beartype
class ProjectSummaryWidgetView(LoginRequiredMixin, TemplateView):
    """Widget view for project summary dashboard partial (HTMX/hyperscript).

    Renders the project summary widget for the user's selected project.
    """

    template_name = "dashboard/widgets/_project_summary.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        dashboard_data = DashboardUserData.objects.filter(user=user).first()
        project_summary = None
        if dashboard_data and dashboard_data.selected_project:
            project_summary = ProjectSummary.objects.filter(
                project_id=dashboard_data.selected_project
            ).first()
        context["project_summary"] = project_summary
        return context


@beartype
class ObligationSummaryWidgetView(LoginRequiredMixin, TemplateView):
    """Widget view for obligation summary dashboard partial (HTMX/hyperscript).

    Renders the obligation summary widget for the user's selected project.
    """

    template_name = "dashboard/widgets/_obligation_summary.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        dashboard_data = DashboardUserData.objects.filter(user=user).first()
        obligation_summary = None
        if dashboard_data and dashboard_data.selected_project:
            project = ProjectSummary.objects.filter(
                project_id=dashboard_data.selected_project
            ).first()
            if project:
                obligation_summary = ObligationSummary.objects.filter(
                    project=project
                ).first()
        context["obligation_summary"] = obligation_summary
        return context


@beartype
class ComplianceMetricsWidgetView(LoginRequiredMixin, TemplateView):
    """Widget view for compliance metrics dashboard partial (HTMX/hyperscript).

    Renders the compliance metrics widget for the user's selected project.
    """

    template_name = "dashboard/widgets/_compliance_metrics.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        dashboard_data = DashboardUserData.objects.filter(user=user).first()
        compliance_metrics = None
        if dashboard_data and dashboard_data.selected_project:
            project = ProjectSummary.objects.filter(
                project_id=dashboard_data.selected_project
            ).first()
            if project:
                compliance_metrics = ComplianceMetrics.objects.filter(
                    project=project
                ).first()
        context["compliance_metrics"] = compliance_metrics
        return context


@beartype
class DashboardUserDataWidgetView(LoginRequiredMixin, TemplateView):
    """Widget view for user-specific dashboard data (HTMX/hyperscript).

    Renders the user data widget for the dashboard.
    """

    template_name = "dashboard/widgets/_user_data.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user_data"] = DashboardUserData.objects.filter(user=user).first()
        return context


@beartype
@method_decorator(ensure_csrf_cookie, name="dispatch")
class DashboardWidgetRefreshView(LoginRequiredMixin, View):
    """Generic HTMX endpoint to refresh a dashboard widget partial by name.

    Args:
        request: The HTTP request object.
        widget: The widget name (e.g., 'project_summary').

    Returns:
        Rendered HTML partial for the requested widget.

    """

    def get(
        self, request: HttpRequest, widget: str, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        widget_map = {
            "project_summary": "dashboard/widgets/_project_summary.html",
            "obligation_summary": "dashboard/widgets/_obligation_summary.html",
            "compliance_metrics": "dashboard/widgets/_compliance_metrics.html",
            "user_data": "dashboard/widgets/_user_data.html",
        }
        template = widget_map.get(widget)
        if not template:
            return JsonResponse({"error": "Unknown widget"}, status=400)
        user = request.user
        dashboard_data = DashboardUserData.objects.filter(user=user).first()
        context = {}
        if widget == "project_summary":
            project_summary = None
            if dashboard_data and dashboard_data.selected_project:
                project_summary = ProjectSummary.objects.filter(
                    project_id=dashboard_data.selected_project
                ).first()
            context["project_summary"] = project_summary
        elif widget == "obligation_summary":
            obligation_summary = None
            if dashboard_data and dashboard_data.selected_project:
                project = ProjectSummary.objects.filter(
                    project_id=dashboard_data.selected_project
                ).first()
                if project:
                    obligation_summary = ObligationSummary.objects.filter(
                        project=project
                    ).first()
            context["obligation_summary"] = obligation_summary
        elif widget == "compliance_metrics":
            compliance_metrics = None
            if dashboard_data and dashboard_data.selected_project:
                project = ProjectSummary.objects.filter(
                    project_id=dashboard_data.selected_project
                ).first()
                if project:
                    compliance_metrics = ComplianceMetrics.objects.filter(
                        project=project
                    ).first()
            context["compliance_metrics"] = compliance_metrics
        elif widget == "user_data":
            context["user_data"] = dashboard_data
        html = render_to_string(template, context, request=request)
        return HttpResponse(html)


@beartype
class DashboardProjectSummaryWidgetView(LoginRequiredMixin, View):
    """HTMX/AJAX view for the project summary widget partial."""

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Return the rendered project summary widget as a partial for HTMX swaps.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: Rendered HTML partial for the widget.

        """
        project_summary = ProjectSummary.objects.first()
        html = render_to_string(
            "dashboard/_dashboard_main.html",
            {
                "project_summary": project_summary,
                "user_projects": ProjectSummary.objects.all(),
            },
            request=request,
        )
        return HttpResponse(html)
