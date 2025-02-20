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
            
            # Get distinct mechanisms for this project
            mechanisms = (Obligation.objects
                        .filter(project=project)
                        .values('primary_environmental_mechanisms')
                        .distinct())
            
            mechanisms_data = []
            for mech in mechanisms:
                name = mech['primary_environmental_mechanisms']
                if not name:
                    continue
                    
                status_counts = (
                    Obligation.objects
                    .filter(
                        project=project,
                        primary_environmental_mechanisms=name
                    )
                    .values('status')
                    .annotate(count=Count('status'))
                    .order_by('status')
                )
                
                mechanisms_data.append({
                    'id': len(mechanisms_data) + 1,
                    'name': name,
                    'status_counts': status_counts
                })
            
            context.update({
                'project': project,
                'mechanisms': mechanisms_data
            })
            
        except Exception as e:
            logger.error(f"Error getting mechanisms data: {str(e)}")
            context['error'] = "Unable to load mechanisms data"
            
        return context

class ChartDataView(LoginRequiredMixin, View):
    """View for fetching chart data via HTMX."""
    
    def get(self, request: HttpRequest, project_id: int, mechanisms: str) -> JsonResponse:
        """Get chart data for a specific mechanisms."""
        try:
            project = get_object_or_404(Project, pk=project_id)
            
            # Get status counts
            data = (Obligation.objects
                   .filter(
                       project=project,
                       primary_environmental_mechanisms=mechanisms
                   )
                   .values('status')
                   .annotate(count=Count('status'))
                   .order_by('status'))
            
            # Format for Chart.js
            chart_data = {
                'type': 'polarArea',
                'data': {
                    'labels': [item['status'].title() for item in data],
                    'datasets': [{
                        'data': [item['count'] for item in data],
                        'backgroundColor': [
                            'rgba(255, 99, 132, 0.5)',
                            'rgba(54, 162, 235, 0.5)',
                            'rgba(255, 206, 86, 0.5)'
                        ]
                    }]
                },
                'options': {
                    'responsive': True,
                    'plugins': {
                        'legend': {
                            'position': 'bottom'
                        }
                    }
                }
            }
            
            return JsonResponse(chart_data)
            
        except Exception as e:
            logger.error(f"Error generating chart data: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)