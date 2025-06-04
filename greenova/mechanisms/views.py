import logging

import matplotlib as mpl
from beartype import beartype
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from matplotlib.figure import Figure
from projects.models import Project

# Optional: Only include these if you want Plotly interactive charts
from .figures import get_mechanism_chart, get_overall_chart
from .models import EnvironmentalMechanism
from .serializers import (
    MechanismCollectionProtoSerializer,
    MechanismProtoSerializer,
)

mpl.use("Agg")  # Use Agg backend for non-interactive plotting

logger = logging.getLogger(__name__)


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class MechanismChartView(LoginRequiredMixin, TemplateView):
    template_name = "mechanisms/mechanism_charts.html"

    @beartype
    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get("project_id")

        if not project_id:
            context["error"] = "No project selected"
            return context

        try:
            project_id = int(project_id)
            if project_id < 1:
                context["error"] = "No project selected"
                return context
        except (TypeError, ValueError):
            context["error"] = "Invalid project ID"
            return context

        try:
            project = Project.objects.get(id=project_id)
            mechanisms = EnvironmentalMechanism.objects.filter(project_id=project_id)
            mechanism_charts = []

            # Add overall chart first
            overall_fig, overall_chart_data = get_overall_chart(project_id)
            mechanism_charts.append(
                {
                    "name": "Overall Status",
                    "image_data": overall_chart_data,
                    "svg_data": self._figure_to_svg(overall_fig),
                },
            )

            # Generate charts for individual mechanisms
            for mechanism in mechanisms:
                fig, chart_data = get_mechanism_chart(mechanism.id)
                mechanism_charts.append(
                    {
                        "id": mechanism.id,
                        "name": mechanism.name,
                        "image_data": chart_data,
                        "svg_data": self._figure_to_svg(fig),
                    },
                )

            context["mechanism_charts"] = mechanism_charts
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
                        m.not_started_count
                        + m.in_progress_count
                        + m.completed_count
                        + m.overdue_count
                    ),
                }
                for m in mechanisms
            ]

        except Project.DoesNotExist:
            context["error"] = f"Project with ID {project_id} not found"
        except Exception as e:
            logger.exception("Error generating mechanism charts: %s", e)
            context["error"] = f"Error generating charts: {e!s}"

        return context

    @beartype
    def _figure_to_svg(self, fig: Figure) -> str:
        """Convert matplotlib figure to SVG string for django_matplotlib integration."""
        import io

        svg_buffer = io.StringIO()
        fig.savefig(
            svg_buffer,
            format="svg",
            bbox_inches="tight",
            facecolor="white",
            edgecolor="none",
        )
        svg_buffer.seek(0)
        svg_string = svg_buffer.getvalue()
        svg_buffer.close()

        # Add interactive chart class for consistency
        return svg_string.replace(
            "<svg",
            '<svg class="interactive-chart mechanism-chart"',
        )


@login_required
def export_mechanism(request, mechanism_id: int) -> "HttpResponse":
    """Export a single mechanism as Protocol Buffer binary data."""
    mechanism = EnvironmentalMechanism.objects.filter(id=mechanism_id).first()
    if not mechanism:
        messages.error(request, "Mechanism not found.")
        return None
    serializer = MechanismProtoSerializer(instance=mechanism)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export mechanism.")
        return None
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = (
        f'attachment; filename="mechanism_{mechanism_id}.pb"'
    )
    return response


@login_required
def export_all_mechanisms(request) -> "HttpResponse":
    """Export all mechanisms as a Protocol Buffer collection."""
    mechanisms = list(EnvironmentalMechanism.objects.all())
    serializer = MechanismCollectionProtoSerializer(instances=mechanisms)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export mechanisms.")
        return None
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="mechanisms.pb"'
    return response


@login_required
@require_http_methods(["GET", "POST"])
def import_mechanism(request) -> "HttpResponse":
    """Import a mechanism from Protocol Buffer binary data."""
    if request.method == "POST":
        if "file" not in request.FILES:
            messages.error(request, "No file was provided.")
            return HttpResponse(status=400)
        uploaded_file = request.FILES["file"]
        try:
            data = uploaded_file.read()
            serializer = MechanismProtoSerializer(data=data)
            if not serializer.is_valid():
                messages.error(
                    request,
                    "Could not deserialize the file. Invalid format.",
                )
                return HttpResponse(status=400)
            mechanism = serializer.validated_data
            mechanism.id = None  # Ensure a new record is created
            mechanism.save()
            messages.success(request, "Mechanism imported successfully.")
            return HttpResponse(status=200)
        except (ValueError, OSError, AttributeError, TypeError):
            messages.error(request, "An error occurred while importing the mechanism.")
            return HttpResponse(status=400)
    # GET request - show import form
    return HttpResponse("Import Mechanism Form")
