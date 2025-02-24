from typing import Dict, Any, List
from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixins import ProjectContextMixin
from projects.models import Project
from obligations.models import Obligation
from django.db.models import Count
from django.http import JsonResponse, HttpRequest
import logging
from django.core.serializers.json import DjangoJSONEncoder
from charts.services import ChartService
from .services import MechanismAnalysisService

logger = logging.getLogger(__name__)


class FilteredMechanismView(View):
    def get(self, request):
        try:
            project_id = request.GET.get("project_id")
            mechanism = request.GET.get("mechanism")

            if not all([project_id, mechanism]):
                raise ValueError("Missing required parameters")

            data = MechanismAnalysisService.get_mechanism_distribution(
                project_id, mechanism
            )

            if not data["datasets"][0]["data"]:
                return JsonResponse({
                    "error": "No data available for this mechanism"
                }, status=404)

            chart_config = ChartService.get_polar_area_config(data)
            return JsonResponse(chart_config)

        except Exception as e:
            logger.error(f"Chart data error: {str(e)}")
            return JsonResponse({
                "error": f"Failed to load chart data: {str(e)}"
            }, status=400)


class MechanismChartView(LoginRequiredMixin, TemplateView):
    """View for displaying mechanism charts."""
    template_name = "mechanisms/mechanism_chart_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'project_id': self.request.GET.get('project_id'),
            'mechanism': self.request.GET.get('mechanism'),
            'chart_endpoint': f'/mechanisms/filtered/?project_id={self.request.GET.get("project_id")}&mechanism={self.request.GET.get("mechanism")}'
        })
        return context
