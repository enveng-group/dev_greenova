from typing import Any, Dict
from django.views.generic import TemplateView, ListView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.db.models import QuerySet, Count
from projects.models import Project, Obligation
from django.conf import settings
from datetime import datetime
import logging
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from utils.mixins import LoggedActionMixin, NavigationMixin
from utils.constants import STATUS_CHOICES, STATUS_NOT_STARTED
from utils.exceptions import ChartDataError
from analytics.data_utils import AnalyticsDataProcessor
from analytics.serializers import ChartDataSerializer

logger = logging.getLogger(__name__)

class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """Main dashboard view."""
    template_name = 'dashboard/views/dashboard.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context

class ProjectDetailView(LoginRequiredMixin, DetailView):
    """Project detail view for the dashboard."""
    model = Project
    template_name = 'project/views/detail.html'
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'

    def get_object(self, queryset=None):
        """Get the project object."""
        return get_object_or_404(Project, pk=self.kwargs.get(self.pk_url_kwarg))

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['obligations'] = Obligation.objects.filter(project=project)
        return context

class ProjectAnalyticsView(LoginRequiredMixin, TemplateView):
    """Analytics view for a specific project."""
    template_name = 'analytics/views/aspect_analysis.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)
        context['project'] = project
        context['analytics'] = project.get_analytics()
        return context

class ProjectSelectionView(LoginRequiredMixin, View):
    """Handle HTMX project selection requests."""
    
    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET request for project selection."""
        try:
            project_id = request.GET.get('project_id')
            if not project_id:
                return JsonResponse({
                    'error': 'No project selected'
                }, status=400)

            project = get_object_or_404(Project, pk=project_id)
            
            # Get unique mechanisms
            mechanisms = (
                project.project_obligations
                .values_list('primary_environmental_mechanism', flat=True)
                .distinct()
            )
            
            # Get obligations with status counts for each mechanism
            mechanism_data = []
            for mechanism in mechanisms:
                status_counts = (
                    project.project_obligations
                    .filter(primary_environmental_mechanism=mechanism)
                    .values('status')
                    .annotate(count=Count('status'))
                )
                
                mechanism_data.append({
                    'name': mechanism,
                    'status_counts': status_counts
                })
            
            context = {
                'project': project,
                'obligations': project.project_obligations.all(),
                'mechanisms': mechanism_data
            }
            
            html = render_to_string(
                'dashboard/views/project_content.html',
                context,
                request
            )
            
            return HttpResponse(html)
            
        except Exception as e:
            logger.error(f"Error in project selection: {str(e)}")
            return JsonResponse({
                'error': 'Failed to load project'
            }, status=500)

@method_decorator(login_required, name='dispatch')
class FilteredObligationsView(LoginRequiredMixin, ListView):
    """View for filtered obligations list."""
    template_name = 'dashboard/components/tables/obligation_list.html'
    context_object_name = 'obligations'

    def get_queryset(self) -> QuerySet[Obligation]:
        """Get filtered queryset of obligations."""
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        queryset = Obligation.objects.filter(project=project)
        
        mechanism = self.request.GET.get('mechanism')
        if mechanism:
            queryset = queryset.filter(primary_environmental_mechanism=mechanism)
            
        return queryset.select_related('project').order_by('action_due_date')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add additional context."""
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('mechanism')
        return context

@method_decorator(csrf_exempt, name='dispatch')
class ChatApiView(View):
    """Handle chat API requests."""

    def get(self, request: HttpRequest) -> JsonResponse:
        """Handle GET requests - return API info."""
        return JsonResponse({
            'status': 'active',
            'message': 'Chat API endpoint is ready',
            'version': '1.0'
        })

    def post(self, request: HttpRequest) -> JsonResponse:
        """Handle POST requests for chat messages."""
        try:
            # Parse and validate request data
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            
            if not message:
                return JsonResponse({
                    "error": "Message is required",
                    "status": "error"
                }, status=400)

            # Process message (placeholder for actual chat logic)
            context = {
                'page': request.GET.get('page', 'unknown'),
                'user': request.user.get_username() if request.user.is_authenticated else 'guest'
            }
            
            response = {
                "status": "success",
                "message": f"I received: {message}",
                "context": context
            }
            
            logger.info(f"Chat message processed: {message[:50]}...")
            return JsonResponse(response)
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON in chat request")
            return JsonResponse({
                "error": "Invalid JSON format",
                "status": "error"
            }, status=400)
            
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            return JsonResponse({
                "error": "Internal server error",
                "status": "error",
                "details": str(e) if settings.DEBUG else None
            }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request: HttpRequest) -> JsonResponse:
    """Legacy function-based view for chat API - redirects to class-based view."""
    view = ChatApiView.as_view()
    response = view(request)
    return JsonResponse(response.content, safe=False)

class ObligationListView(LoginRequiredMixin, TemplateView):
    """View for listing project obligations."""
    template_name = 'dashboard/obligation_list.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        context['obligations'] = Obligation.objects.filter(project_id=project_id)
        return context