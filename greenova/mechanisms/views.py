"""
Views for the mechanisms app.

This module provides views for handling environmental mechanism data
and related visualizations.
"""

import logging
from typing import (  # Keep Dict if used, ensure Optional is imported if str
    Any,
)

import matplotlib
from beartype import beartype
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import ListView, TemplateView
from figures import get_mechanism_plotly_chart, get_overall_plotly_chart
from models import EnvironmentalMechanism
from obligations.constants import (
    STATUS_COMPLETED,
    STATUS_IN_PROGRESS,
    STATUS_NOT_STARTED,
    STATUS_OVERDUE,
)
from obligations.models import Obligation
from projects.models import Project

matplotlib.use("Agg")  # Use Agg backend for non-interactive plotting

logger = logging.getLogger(__name__)


@method_decorator(cache_control(max_age=60), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ObligationInsightView(LoginRequiredMixin, TemplateView):
    """View for providing obligation insights for chart segments on hover.

    This view returns information about obligations for a specific mechanism and status
    combination, used for tooltips when users hover over chart segments in the
    interactive plotly charts.
    """

    template_name = "mechanisms/partials/_obligation_insight.html"

    @beartype  # type: ignore[misc]
    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse | HttpResponse:
        """Handle GET requests and return appropriate format (HTML or JSON).

        Supports both traditional HTML response and JSON for Plotly integration.

        Args:
            request: The HTTP request
            *args: Variable positional arguments
            **kwargs: Variable keyword arguments

        Returns:
            Either a JSON response or standard HTML template response
        """
        response_format = request.GET.get("format", "html").lower()

        if response_format == "json":
            context = self.get_context_data(**kwargs)

            # Remove error message from JSON if present
            error = context.pop("error", None)

            if error:
                return JsonResponse({"error": error}, status=400)

            # Format obligations for JSON response
            if "obligations" in context:
                obligations_data = []
                for obligation in context["obligations"]:
                    obligations_data.append(
                        {
                            "number": obligation.obligation_number,
                            "due_date": (
                                obligation.action_due_date.strftime("%Y-%m-%d")
                                if obligation.action_due_date
                                else None
                            ),
                            "close_out_date": (
                                obligation.close_out_date.strftime("%Y-%m-%d")
                                if obligation.close_out_date
                                else None
                            ),
                        }
                    )
                context["obligations"] = obligations_data

            return JsonResponse(context)

        # Default to HTML response
        return super().get(request, *args, **kwargs)

    @beartype  # type: ignore[misc]
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data for the obligation insight template.

        Retrieves obligation data for a specific mechanism and status combination to
        display in hover tooltips on mechanism charts.

        Args:
            **kwargs: Keyword arguments from the URL dispatch.

        Returns:
            Context dictionary with obligation data.
        """
        context = super().get_context_data(**kwargs)

        mechanism_id_str: str | None = self.request.GET.get("mechanism_id")
        status: str | None = self.request.GET.get("status")

        if not mechanism_id_str or not status:
            context["error"] = "Missing required parameters"
            return context

        try:
            mechanism_id: int = int(mechanism_id_str)

            # Map frontend status keys to database status values
            status_map: dict[str, str] = {
                "not_started": STATUS_NOT_STARTED,
                "in_progress": STATUS_IN_PROGRESS,
                "completed": STATUS_COMPLETED,
                "overdue": STATUS_OVERDUE,
            }

            status_key: str = status.lower().replace(" ", "_")
            if status_key not in status_map:
                context["error"] = f"Invalid status: {status}"
                return context

            status_value: str = status_map[status_key]

            # Query obligations based on mechanism ID and status
            obligations = Obligation.objects.filter(
                primary_environmental_mechanism_id=mechanism_id, status=status_value
            ).order_by("action_due_date")

            # Count total obligations matching criteria
            total_count: int = obligations.count()

            # Get the first 5 obligations for the tooltip
            obligations_preview = obligations[:5]

            context.update(
                {
                    "mechanism_id": mechanism_id,
                    "status": status,
                    "status_key": status_key,
                    "count": total_count,
                    "total_count": total_count,
                    "obligations": obligations_preview,
                }
            )

        except (ValueError, TypeError) as e:
            logger.warning("Invalid parameters for obligation insights: %s", str(e))
            context["error"] = f"Invalid parameters: {e!s}"
        except Exception as e:
            logger.error("Error fetching obligation insights: %s", str(e))
            context["error"] = "An error occurred while fetching obligation insights"

        return context


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class MechanismChartView(LoginRequiredMixin, TemplateView):
    """View for displaying mechanism charts for a selected project.

    This view generates and provides interactive Plotly charts for the overall project
    status and for each environmental mechanism within the selected project.
    """

    template_name = "mechanisms/mechanism_charts.html"

    @beartype  # type: ignore[misc]
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data for rendering mechanism charts.

        Retrieves the project, mechanisms, and generates chart HTML for both the overall
        project status and each individual mechanism.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            Context dictionary with chart data and project information.
        """
        context = super().get_context_data(**kwargs)
        project_id_str: str | None = self.request.GET.get("project_id")

        if not project_id_str:
            context["error"] = "No project selected"
            return context

        try:
            project_id: int = int(project_id_str)
            if project_id < 1:
                context["error"] = "No project selected"
                return context
        except (TypeError, ValueError):
            context["error"] = "Invalid project ID"
            return context

        try:
            # Check if project exists
            project = Project.objects.get(id=project_id)
            mechanisms = EnvironmentalMechanism.objects.filter(project_id=project_id)
            mechanism_charts = []

            # Add overall chart first (plotly)
            overall_chart_html = get_overall_plotly_chart(project_id)
            mechanism_charts.append(
                {
                    "name": "Overall Status",
                    "chart_html": overall_chart_html,
                }
            )

            # Generate charts for individual mechanisms (plotly)
            for mechanism in mechanisms:
                chart_html = get_mechanism_plotly_chart(mechanism.id)
                mechanism_charts.append(
                    {
                        "id": mechanism.id,
                        "name": mechanism.name,
                        "chart_html": chart_html,
                    }
                )

            context["mechanism_charts"] = mechanism_charts
            context["project"] = project

            # Add table data with mechanism ID
            context["table_data"] = [
                {
                    "id": m.id,
                    "name": m.name,
                    "not_started": m.not_started_count,
                    "in_progress": m.in_progress_count,
                    "completed": m.completed_count,
                    "overdue": m.overdue_count,
                }
                for m in mechanisms
            ]
            return context
        except Project.DoesNotExist:
            context["error"] = "Project not found"
            return context
        except Exception as e:
            logger.error("Error generating mechanism charts: %s", str(e))
            context["error"] = "An error occurred while generating charts"
            return context


class MechanismListView(LoginRequiredMixin, ListView):
    """List all environmental mechanisms.

    Displays a list of all environmental mechanisms in the system.
    """

    model = EnvironmentalMechanism
    template_name = "mechanisms/mechanisms_list.html"
    context_object_name = "mechanisms"

    @beartype  # type: ignore[misc]
    def get_queryset(self) -> QuerySet[EnvironmentalMechanism]:
        """Return the queryset of all environmental mechanisms.

        Returns:
            Queryset of EnvironmentalMechanism objects.
        """
        return EnvironmentalMechanism.objects.all()
