from typing import Dict, Any, List
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixins import ProjectContextMixin
from projects.models import Project
from obligations.models import Obligation
from django.db.models import Count
from django.http import JsonResponse, HttpRequest
import logging
from django.core.serializers.json import DjangoJSONEncoder

logger = logging.getLogger(__name__)


class FilteredMechanismView(LoginRequiredMixin, TemplateView):
    """Handle filtered mechanism data requests."""

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        try:
            project_id = request.GET.get('project_id')
            mechanism = request.GET.get('mechanism')

            if not project_id:
                return JsonResponse({'error': 'Project ID required'}, status=400)

            project = get_object_or_404(Project, id=project_id)

            # Get status distribution for mechanism
            status_data = (Obligation.objects
                         .filter(
                             project=project,
                             primary_environmental_mechanism=mechanism
                         )
                         .values('status')
                         .annotate(count=Count('status'))
                         .order_by('status'))

            # Log the query and results for debugging
            logger.debug(f"Query: {status_data.query}")
            logger.debug(f"Results: {list(status_data)}")

            chart_items: List[Dict[str, Any]] = [{
                'label': item['status'].title(),  # Capitalize status
                'value': item['count'],
                'color': self._get_status_color(item['status'])
            } for item in status_data]

            chart_data: Dict[str, Any] = {
                'type': 'polarArea',
                'data': {
                    'labels': [item['label'] for item in chart_items],
                    'datasets': [{
                        'data': [item['value'] for item in chart_items],
                        'backgroundColor': [item['color'] for item in chart_items],
                        'borderColor': 'rgba(255, 255, 255, 0.5)',
                        'borderWidth': 1
                    }]
                }
            }

            # Log the final chart data for debugging
            logger.debug(f"Chart data: {chart_data}")

            return JsonResponse(chart_data, encoder=DjangoJSONEncoder)

        except Exception as e:
            logger.error(f"Error in FilteredMechanismView: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    def _get_status_color(self, status: str) -> str:
        """Get color for status."""
        colors: Dict[str, str] = {
            'not started': 'rgba(108, 117, 125, 0.8)',  # gray
            'in progress': 'rgba(0, 123, 255, 0.8)',    # blue
            'completed': 'rgba(40, 167, 69, 0.8)'       # green
        }
        return colors.get(status.lower(), 'rgba(108, 117, 125, 0.8)')


class MechanismChartView(LoginRequiredMixin, ProjectContextMixin, TemplateView):
    """Main mechanism chart view."""
    template_name = 'mechanisms/mechanism_charts.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            project_id = self.request.GET.get('project_id')
            if project_id:
                project = get_object_or_404(Project, id=project_id)

                # Get unique mechanisms
                mechanisms = (Obligation.objects
                           .filter(project=project)
                           .values_list('primary_environmental_mechanism', flat=True)
                           .distinct()
                           .order_by('primary_environmental_mechanism'))

                context.update({
                    'project': project,
                    'mechanisms': mechanisms
                })

        except Exception as e:
            logger.error(f"Error getting mechanism chart data: {str(e)}")
            context['error'] = str(e)

        return context
