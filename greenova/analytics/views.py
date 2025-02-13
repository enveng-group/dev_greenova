from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.db.models import Count
from typing import Dict, Any, TypedDict
from projects.models import Obligation
from utils.mixins import LoggedActionMixin
from .generics import AnalyticsView  # Add this import

class StatusCount(TypedDict):
    status: str
    count: int

class AnalyticsDashboardView(LoggedActionMixin, TemplateView):
    template_name = 'analytics/views/mechanism_dashboard.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        mechanisms = (Obligation.objects
                     .values('primary_environmental_mechanism')
                     .annotate(total=Count('id'))
                     .order_by('primary_environmental_mechanism'))
        context['mechanisms'] = mechanisms
        return context

class MechanismStatusChartView(LoggedActionMixin, TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        raw_counts = (Obligation.objects
                     .values('status')
                     .annotate(count=Count('id')))
        
        counts: Dict[str, int] = {
            'not started': 0,
            'in progress': 0,
            'completed': 0
        }
        
        for item in raw_counts:
            if isinstance(item['status'], str):
                counts[item['status']] = item['count']
        
        data: Dict[str, list[str] | list[int]] = {
            'labels': ['Not Started', 'In Progress', 'Completed'],
            'values': [
                counts['not started'],
                counts['in progress'],
                counts['completed']
            ]
        }
        
        return JsonResponse(data)

class AspectAnalyticsView(LoggedActionMixin, TemplateView):
    template_name = 'analytics/views/aspect_analysis.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        aspects = (Obligation.objects
                  .values('environmental_aspect')
                  .annotate(total=Count('id'))
                  .order_by('environmental_aspect'))
        context['aspects'] = aspects
        return context

class AspectDetailsView(AnalyticsView[Obligation]):
    """View for displaying aspect details."""
    template_name = 'analytics/views/aspect_details.html'
    model = Obligation