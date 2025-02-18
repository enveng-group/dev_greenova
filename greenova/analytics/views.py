from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.db.models import Count
from typing import Dict, Any, TypedDict
from obligations.models import Obligation
from utils.mixins import LoggedActionMixin
from utils.constants import STATUS_CHOICES
from utils.generics import AnalyticsView
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from projects.models import Project

# Set up logger
logger = logging.getLogger(__name__)

class AnalyticsDashboardView(LoggedActionMixin, TemplateView):
    template_name = 'analytics/views/mechanism_dashboard.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        mechanisms = (Obligation.objects
                     .values('primary_environmental_mechanism')
                     .annotate(total=Count('id'))
                     .order_by('primary_environmental_mechanism'))
        context['mechanisms'] = mechanisms
        

        status_counts = {
            'not_started': Obligation.objects.filter(status='Not Started').count(),
            'in_progress': Obligation.objects.filter(status='In Progress').count(),
            'completed': Obligation.objects.filter(status='Completed').count(),
        }
        context['status_counts'] = status_counts

        return context

class MechanismStatusChartView(LoggedActionMixin, TemplateView):
    """View for getting mechanism status chart data."""
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET request for mechanism status data."""
        try:
            mechanism = request.GET.get('mechanism')
            if not mechanism:
                return JsonResponse(
                    {'error': 'Mechanism parameter is required'}, 
                    status=400
                )

            # Get raw counts from database
            raw_counts = (Obligation.objects
                        .filter(primary_environmental_mechanism=mechanism)
                        .values('status')
                        .annotate(count=Count('id')))
            
            # Initialize counts dictionary with all possible statuses
            counts: Dict[str, int] = {
                status[0]: 0 for status in STATUS_CHOICES
            }
            
            # Update counts with actual values
            for item in raw_counts:
                if item['status'] in counts:
                    counts[item['status']] = item['count']
            
            # Format data for Chart.js
            data = {
                'type': 'doughnut',
                'data': {
                    'labels': [status[1] for status in STATUS_CHOICES],
                    'datasets': [{
                        'data': [counts[status[0]] for status in STATUS_CHOICES],
                        'backgroundColor': [
                            'var(--error)',    # Not Started
                            'var(--primary)',  # In Progress
                            'var(--success)'   # Completed
                        ]
                    }]
                },
                'options': {
                    'responsive': True,
                    'maintainAspectRatio': True,
                    'plugins': {
                        'legend': {
                            'position': 'bottom'
                        }
                    }
                }
            }
            
            logger.debug(f"Generated chart data for mechanism: {mechanism}")
            return JsonResponse(data)
            
        except Exception as e:
            logger.error(f"Error generating chart data: {str(e)}")
            return JsonResponse(
                {'error': 'Error generating chart data'}, 
                status=500
            )

class AspectAnalyticsView(LoggedActionMixin, TemplateView):
    """View for aspect analysis."""
    template_name = 'analytics/views/aspect_analysis.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add aspect analysis context data."""
        try:
            context = super().get_context_data(**kwargs)
            aspects = (Obligation.objects
                      .values('environmental_aspect')
                      .annotate(total=Count('id'))
                      .order_by('environmental_aspect'))
            context['aspects'] = aspects
            return context
        except Exception as e:
            logger.error(f"Error getting aspect analysis data: {str(e)}")
            raise

class AspectDetailsView(AnalyticsView[Obligation]):
    """View for displaying aspect details."""
    template_name = 'analytics/views/aspect_details.html'
    model = Obligation

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add aspect details context data."""
        try:
            context = super().get_context_data(**kwargs)
            aspect = self.kwargs.get('aspect')
            if aspect:
                obligations = (self.model.objects
                             .filter(environmental_aspect=aspect)
                             .select_related('project'))
                context['obligations'] = obligations
            return context
        except Exception as e:
            logger.error(f"Error getting aspect details: {str(e)}")
            raise

def home_router(request):
    """Route to appropriate home page based on auth status."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return redirect('landing:home')

class AspectAnalysisView(LoggedActionMixin, LoginRequiredMixin, TemplateView):
    """View for analyzing environmental aspects of a project."""
    template_name = 'analytics/views/aspect_analysis.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Get context data including project analytics."""
        context = super().get_context_data(**kwargs)
        try:
            project = get_object_or_404(Project, id=self.kwargs.get('project_id'))
            context['project'] = project
            context['analytics'] = project.get_analytics()
            
            # Add aspect analysis specific data
            aspects = (project.obligations
                      .values('environmental_aspect')
                      .annotate(total=Count('id'))
                      .order_by('environmental_aspect'))
            context['aspects'] = aspects
            
            return context
            
        except Exception as e:
            logger.error(f"Error in AspectAnalysisView: {str(e)}")
            context['error'] = "Error loading aspect analysis"
            return context