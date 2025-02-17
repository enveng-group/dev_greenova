from typing import Any, Dict
from django.views.generic import TemplateView, ListView, View
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
from utils.constants import STATUS_CHOICES
from utils.exceptions import ChartDataError
from analytics.data_utils import AnalyticsDataProcessor
from analytics.serializers import ChartDataSerializer

logger = logging.getLogger(__name__)

class DashboardHomeView(LoggedActionMixin, NavigationMixin, TemplateView):
    """Main dashboard view."""
    template_name = 'dashboard/views/dashboard.html'
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add dashboard context data."""
        context = super().get_context_data(**kwargs)
        try:
            user = self.request.user
            projects = Project.objects.all()
            processor = AnalyticsDataProcessor(Obligation.objects.all())
            
            context.update({
                'projects': projects,
                'analytics': processor.get_mechanism_data('all'),
                'system_status': self.get_system_status(),
                'app_version': getattr(settings, 'APP_VERSION', '1.0.0'),
                'last_updated': datetime.now(),
                'user_name': user.get_username()
            })
            return context
        except Exception as e:
            logger.error(f"Error getting dashboard data: {str(e)}")
            raise
    
    def get_system_status(self) -> str:
        """Determine current system status."""
        try:
            # Implement actual status checks here
            return 'operational'
        except Exception as e:
            logger.error(f"System status check error: {str(e)}")
            return 'error'

class ProjectSelectorView(LoggedActionMixin, NavigationMixin, View):
    """Handle project selection and return project-specific content."""
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET request for project selection."""
        try:
            project_id = request.GET.get('project_id')
            project = get_object_or_404(Project, id=project_id)
            
            # Get filtered obligations using utils
            from analytics.filters import ObligationFilter
            obligation_filter = ObligationFilter(project.obligations.all())
            obligations = obligation_filter.filter_by_status(STATUS_NOT_STARTED)
            
            context = {
                'project': project,
                'obligations': obligations,
                'mechanisms': project.obligations.values(
                    'primary_environmental_mechanism'
                ).distinct()
            }
            
            return render(request, 'dashboard/views/project_content.html', context)
        except Exception as e:
            logger.error(f"Project selection error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

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

class ObligationListView(LoginRequiredMixin, ListView):
    """View for displaying obligations list."""
    template_name = 'dashboard/components/tables/obligation_list.html'
    context_object_name = 'obligations'

    def get_queryset(self) -> QuerySet[Obligation]:
        """Get queryset of obligations for the selected project."""
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, pk=project_id)
        return (Obligation.objects
                .filter(project=project)
                .select_related('project')
                .order_by('action_due_date'))

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        context.update({
            'project_id': self.kwargs.get('project_id'),
            'current_filter': self.request.GET.get('mechanism')
        })
        return context