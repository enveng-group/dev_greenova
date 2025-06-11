import logging
import json
import matplotlib
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import ListView, TemplateView
from projects.models import Project
from django.http import JsonResponse
from .figures import get_mechanism_chart, get_overall_chart
from .models import EnvironmentalMechanism
from obligations.models import Obligation
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.safestring import mark_safe
matplotlib.use("Agg")  # Use Agg backend for non-interactive plotting

logger = logging.getLogger(__name__)


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class MechanismChartView(LoginRequiredMixin, TemplateView):
    template_name = "mechanisms/mechanism_charts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get("project_id")

        if not project_id or not project_id.isdigit():
            context["error"] = "Invalid or missing project ID"
            return context

        project_id = int(project_id)

        try:
            project = Project.objects.get(id=project_id)
            mechanisms = EnvironmentalMechanism.objects.filter(project_id=project_id)

            if not mechanisms.exists():
                context["error"] = "No mechanisms found for this project"
                return context

            # Prepare chart data (labels & datasets for Chart.js)
            mechanism_chart_data = []

            # Add overall chart data
            total_not_started = sum(m.not_started_count for m in mechanisms)
            total_in_progress = sum(m.in_progress_count for m in mechanisms)
            total_completed = sum(m.completed_count for m in mechanisms)
            total_overdue = sum(m.overdue_count for m in mechanisms)
            overall_data = {
                "id": "overall",
                "name": "Overall Status",
                "labels": ["Not Started", "In Progress", "Completed", "Overdue"],
                "data": [
                    total_not_started,
                    total_in_progress,
                    total_completed,
                    total_overdue,
                ],
            }
            mechanism_chart_data.append(overall_data)
            # Individual mechanism charts
            for mech in mechanisms:
                data = {
                    "id": mech.id,
                    "name": mech.name,
                    "labels": ["Not Started", "In Progress", "Completed", "Overdue"],
                    "data": [
                        mech.not_started_count,
                        mech.in_progress_count,
                        mech.completed_count,
                        mech.overdue_count,
                    ],
                }
                mechanism_chart_data.append(data)

            context["mechanism_charts"] = mechanism_chart_data
            context["mechanism_charts_json"] = mark_safe(json.dumps(mechanism_chart_data))
            context["project"] = project

            context["table_data"] = [
                {
                    "id": m.id,
                    "name": m.name,
                    "not_started": m.not_started_count,
                    "in_progress": m.in_progress_count,
                    "completed": m.completed_count,
                    "overdue": m.overdue_count,
                    "total": (
                        m.not_started_count +
                        m.in_progress_count +
                        m.completed_count +
                        m.overdue_count
                    ),
                }
                for m in mechanisms
            ]

        except Project.DoesNotExist:
            context["error"] = f"Project with ID {project_id} not found"
        except Exception as e:
            logger.exception("Error generating mechanism charts")
            context["error"] = f"Unexpected error: {str(e)}"

        return context


class MechanismListView(LoginRequiredMixin, ListView):
    """List all environmental mechanisms."""

    model = EnvironmentalMechanism
    template_name = "mechanisms/mechanisms_list.html"
    context_object_name = "mechanisms"

    def get_queryset(self):
        return EnvironmentalMechanism.objects.all()

# Optional: JSON endpoint for Chart.js AJAX loading
def mechanism_chart_data_json(request):
    project_id = request.GET.get("project_id")

    if not project_id or not project_id.isdigit():
        return HttpResponseBadRequest("Invalid or missing project_id")

    project_id = int(project_id)
    try:
        mechanisms = EnvironmentalMechanism.objects.filter(project_id=project_id)
        if not mechanisms.exists():
            return JsonResponse([] , safe=False)

        total_not_started = sum(m.not_started_count for m in mechanisms)
        total_in_progress = sum(m.in_progress_count for m in mechanisms)
        total_completed = sum(m.completed_count for m in mechanisms)
        total_overdue = sum(m.overdue_count for m in mechanisms)

        charts = [{
            "id": "overall",
            "name": "Overall Status",
            "labels": ["Not Started", "In Progress", "Completed", "Overdue"],
            "data": [
                total_not_started,
                total_in_progress,
                total_completed,
                total_overdue,
            ],
        }]

        for mech in mechanisms:
            charts.append({
                "id": mech.id,
                "name": mech.name,
                "labels": ["Not Started", "In Progress", "Completed", "Overdue"],
                "data": [
                    mech.not_started_count,
                    mech.in_progress_count,
                    mech.completed_count,
                    mech.overdue_count,
                ],
            })

        return JsonResponse(charts, safe=False)
    except Exception as e:
        logger.error(f"Error loading chart data: {e}")
        return JsonResponse({"error": "Unable to load chart data"}, status=500)
