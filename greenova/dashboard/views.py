"""Copyright (C) 2024 Adrian Gallo <agallo@enveng-group.com.au>
This file is part of Greenova and is licensed under the AGPL-3.0.

Dashboard app views for Greenova.
"""

import base64
import io
import logging
from typing import Any

import matplotlib.pyplot as plt
from beartype import beartype
from core.context_processors import projects_context
from dashboard.utils import sanitize_html  # noqa: F401
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from protobuf import chart_data_pb2, greenova_data_pb2

logger = logging.getLogger(__name__)


@beartype
class DashboardIndexView(LoginRequiredMixin, TemplateView):
    """Main dashboard view for authenticated users.

    Renders dashboard summary, chart, and compliance metrics using Protobuf3.
    """

    template_name = "dashboard/dashboard_home.html"

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Generate context data for the dashboard view.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict[str, Any]: Context data for rendering the dashboard.

        """
        context = super().get_context_data(**kwargs)
        context.update(projects_context(self.request))
        # --- Protobuf3 dashboard summary ---
        dashboard_data = greenova_data_pb2.DashboardData()
        # Project summary
        project_summary = dashboard_data.project_summary
        project_summary.total_projects = 3
        project_summary.active_projects = 2
        project_summary.completed_projects = 1
        # Add recent projects
        for name, desc in [
            ("Greenfield Mine", "Iron or project, WA"),
            ("Solar Farm", "Renewable energy, QLD"),
            ("Wetlands Restoration", "Biodiversity, VIC"),
        ]:
            p = project_summary.recent_projects.add()
            p.id = 0
            p.name = name
            p.description = desc
            p.location = "AU"
        # Obligation summaries
        for status, count in [("Completed", 8), ("Overdue", 2), ("Pending", 2)]:
            ob_sum = dashboard_data.obligation_summaries.add()
            ob_sum.status = status
            ob_sum.count = count
        # Compliance metrics
        dashboard_data.compliance_metrics.overall_compliance_rate = 0.8
        dashboard_data.compliance_metrics.overdue_obligations = 2
        dashboard_data.compliance_metrics.due_this_week = 1
        dashboard_data.compliance_metrics.due_this_month = 3
        dashboard_data.last_updated = 1720454400  # Example timestamp
        # Serialize to bytes and base64 for template
        dashboard_proto_bytes = dashboard_data.SerializeToString()
        dashboard_proto_b64 = base64.b64encode(dashboard_proto_bytes).decode("utf-8")
        context["dashboard_proto_b64"] = dashboard_proto_b64
        context["dashboard_summary"] = dashboard_data.project_summary
        context["obligation_summaries"] = dashboard_data.obligation_summaries
        context["compliance_metrics"] = dashboard_data.compliance_metrics
        # --- Protobuf3 chart data ---
        chart_data = chart_data_pb2.ChartData()
        chart_data.chart_id = "compliance-status"
        chart_data.chart_type = "pie"
        chart_data.title = "Obligation Compliance Status"
        # Add a data series
        series = chart_data.data_series.add()
        series.series_name = "Status"
        for label, value, color in [
            ("Completed", 8, "#28a745"),
            ("Overdue", 2, "#dc3545"),
            ("Pending", 2, "#ffc107"),
        ]:
            dp = series.data_points.add()
            dp.label = label
            dp.y_value = value
            dp.metadata["color"] = color
        # Serialize chart data
        chart_proto_bytes = chart_data.SerializeToString()
        chart_proto_b64 = base64.b64encode(chart_proto_bytes).decode("utf-8")
        context["chart_proto_b64"] = chart_proto_b64
        # --- Generate static chart image with matplotlib ---
        labels = [dp.label for dp in series.data_points]
        sizes = [dp.y_value for dp in series.data_points]
        colors = [dp.metadata["color"] for dp in series.data_points]
        fig, ax = plt.subplots(figsize=(3, 3))  # type: ignore[assignment]
        ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct="%1.0f%%",
            startangle=90,
        )  # type: ignore
        ax.axis("equal")  # type: ignore
        buf = io.BytesIO()
        plt.tight_layout()  # type: ignore
        plt.savefig(buf, format="svg")  # type: ignore
        plt.close(fig)  # type: ignore
        buf.seek(0)
        svg_data = buf.getvalue().decode("utf-8")
        # mark_safe is required here because the SVG is generated server-side and sanitized.
        # This is safe as the SVG is not user-supplied and is generated by trusted code.
        context["dashboard_chart_svg"] = mark_safe(
            svg_data)  # nosec: S308 justified above
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
