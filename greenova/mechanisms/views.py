from typing import Any, Dict
import logging
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from django.db.models import Count
from projects.models import Project
from obligations.models import Obligation
from utils.mixins import LoggedActionMixin

logger = logging.getLogger(__name__)

class mechanismsChartView(LoggedActionMixin, LoginRequiredMixin, TemplateView):
    """View for displaying mechanisms charts."""
    template_name = 'mechanisms/mechanisms_charts.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Get context data including project and mechanisms data."""
        context = super().get_context_data(**kwargs)

        try:
            project_id = self.kwargs.get('project_id')
            project = get_object_or_404(Project, pk=project_id)
            context['project'] = project

            # Get distinct mechanisms with status counts
            mechanisms_data = []
            status_counts = (
                Obligation.objects
                .filter(project=project)
                .values('primary_environmental_mechanisms')
                .annotate(
                    total=Count('id'),
                    not_started=Count('id', filter=Q(status='not started')),
                    in_progress=Count('id', filter=Q(status='in progress')),
                    completed=Count('id', filter=Q(status='completed'))
                )
                .exclude(primary_environmental_mechanisms='')
                .order_by('primary_environmental_mechanisms')
            )

            for mech in status_counts:
                name = mech['primary_environmental_mechanisms']
                mechanisms_data.append({
                    'name': name,
                    'id': name.lower().replace(' ', '-'),
                    'total': mech['total'],
                    'status_counts': {
                        'Not Started': mech['not_started'],
                        'In Progress': mech['in_progress'],
                        'Completed': mech['completed']
                    }
                })

            context['mechanisms'] = mechanisms_data

        except Exception as e:
            logger.error(f"Error getting mechanisms data: {str(e)}")
            context['error'] = "Unable to load mechanisms data"

        return context

class ChartDataView(LoginRequiredMixin, View):
    """View for fetching chart data via HTMX."""

    def get(self, request: HttpRequest, project_id: int, mechanism: str) -> JsonResponse:
        """Get chart data for a specific mechanism."""
        try:
            project = get_object_or_404(Project, pk=project_id)

            # Get status counts for mechanism
            status_counts = (
                Obligation.objects
                .filter(
                    project=project,
                    primary_environmental_mechanisms=mechanism
                )
                .values('status')
                .annotate(count=Count('id'))
                .order_by('status')
            )

            # Prepare chart data
            chart_data = {
                'type': 'doughnut',
                'data': {
                    'labels': ['Not Started', 'In Progress', 'Completed'],
                    'datasets': [{
                        'data': [
                            next((item['count'] for item in status_counts
                                 if item['status'] == 'not started'), 0),
                            next((item['count'] for item in status_counts
                                 if item['status'] == 'in progress'), 0),
                            next((item['count'] for item in status_counts
                                 if item['status'] == 'completed'), 0)
                        ],
                        'backgroundColor': [
                            '#ff6b6b',  # Red for Not Started
                            '#339af0',  # Blue for In Progress
                            '#51cf66'   # Green for Completed
                        ]
                    }]
                },
                'options': {
                    'responsive': True,
                    'maintainAspectRatio': True,
                    'plugins': {
                        'legend': {
                            'position': 'bottom'
                        },
                        'title': {
                            'display': True,
                            'text': f'Status Distribution - {mechanism}'
                        }
                    }
                }
            }

            return JsonResponse(chart_data)

        except Exception as e:
            logger.error(f"Error getting chart data: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)
