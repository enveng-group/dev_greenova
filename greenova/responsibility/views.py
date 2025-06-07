"""Views for the responsibility app.

This module provides views for displaying, exporting, and importing
responsibility data, including chart rendering and API endpoints.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import logging
from typing import Any

from beartype import beartype
from core.utils.roles import (
    get_responsibility_choices,
    get_responsibility_display_name,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView, View
from obligations.models import Obligation

from .figures import generate_responsibility_chart
from .models import Responsibility
from .serializers import (
    ResponsibilityCollectionProtoSerializer,
    ResponsibilityProtoSerializer,
)

logger = logging.getLogger(__name__)


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ResponsibilityChartView(LoginRequiredMixin, TemplateView):
    """View for displaying responsibility charts."""

    template_name = "responsibility/responsibility_chart.html"

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data for the responsibility chart view.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict[str, Any]: Context data for the template.

        """
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get("project_id")

        if not project_id:
            context["error"] = "No project selected"
            return context

        try:
            obligations = Obligation.objects.filter(project_id=project_id)
            responsibility_counts: dict[str, int] = {}

            for obligation in obligations:
                resp_display = get_responsibility_display_name(
                    obligation.responsibility,
                )
                if resp_display not in responsibility_counts:
                    responsibility_counts[resp_display] = 0
                responsibility_counts[resp_display] += 1

            chart_data = generate_responsibility_chart(responsibility_counts)
            context["responsibility_data"] = responsibility_counts
            context["chart_data"] = chart_data
            context["project_id"] = project_id

        except Exception as e:
            logger.exception("Error generating responsibility chart: %s", e)
            context["error"] = f"Error generating chart: {e!s}"

        return context


class ResponsibilityChartApiView(View):
    """API View for displaying the responsibility chart."""

    @beartype
    def get(
        self,
        request: HttpRequest,
        *args: object,
        **kwargs: object,
    ) -> HttpResponse:
        """Handle GET requests for the responsibility chart API.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The HTTP response with the rendered chart.

        """
        # Stub: Implement API logic here
        return JsonResponse({"detail": "Not implemented"}, status=501)


@beartype
@require_GET
def get_responsibility_options(request: HttpRequest) -> HttpResponse:
    """Get available responsibility options.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The HTTP response with options data.

    """
    choices = get_responsibility_choices()
    options = [{"value": value, "display": display} for value, display in choices]
    return JsonResponse({"options": options})


@beartype
@login_required
@require_http_methods(["GET"])
def export_responsibility(
    request: HttpRequest,
    responsibility_id: int,
) -> HttpResponse:
    """Export a single responsibility.

    Args:
        request: The HTTP request object.
        responsibility_id: The ID of the responsibility to export.

    Returns:
        HttpResponse: The HTTP response with the exported data.

    """
    responsibility = get_object_or_404(Responsibility, id=responsibility_id)
    serializer = ResponsibilityProtoSerializer(instance=responsibility)
    data = serializer.data()
    if not data:
        return JsonResponse({"error": "Failed to export responsibility."}, status=400)
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = (
        f'attachment; filename="responsibility_{responsibility_id}.pb"'
    )
    return response


@beartype
@login_required
@require_http_methods(["GET"])
def export_all_responsibilities(request: HttpRequest) -> HttpResponse:
    """Export all responsibilities.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The HTTP response with the exported data.

    """
    responsibilities = list(Responsibility.objects.all())
    serializer = ResponsibilityCollectionProtoSerializer(instances=responsibilities)
    data = serializer.data()
    if not data:
        return JsonResponse({"error": "Failed to export responsibilities."}, status=400)
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="responsibilities.pb"'
    return response


@beartype
@csrf_exempt
@login_required
@require_http_methods(["POST"])
def import_responsibility(request: HttpRequest) -> HttpResponse:
    """Import responsibilities from a file.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The HTTP response after importing.

    """
    data = request.body
    serializer = ResponsibilityProtoSerializer(data=data)
    if not serializer.is_valid():
        return JsonResponse({"error": serializer.errors}, status=400)
    responsibility = serializer.save()
    return JsonResponse(
        {
            "id": responsibility.id,
            "message": "Responsibility imported successfully.",
        },
    )
