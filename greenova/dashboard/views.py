from typing import Any, Dict
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from django.db.models import QuerySet
from projects.models import Project, Obligation
from django.conf import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """Main dashboard view."""
    template_name = 'dashboard/views/dashboard.html'
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add dashboard context data."""
        context = super().get_context_data(**kwargs)
        try:
            context.update({
                'projects': Project.objects.all(),
                'system_status': self.get_system_status(),
                'app_version': getattr(settings, 'APP_VERSION', '1.0.0'),
                'last_updated': datetime.now()
            })
        except Exception as e:
            logger.error(f"Dashboard context error: {str(e)}")
            context['error'] = 'Error loading dashboard data'
        return context
    
    def get_system_status(self) -> str:
        """Determine current system status."""
        try:
            # Implement actual status checks here
            return 'operational'
        except Exception as e:
            logger.error(f"System status check error: {str(e)}")
            return 'error'

@method_decorator(login_required, name='dispatch')
class ProjectSelectorView(TemplateView):
    """Handle project selection."""
    template_name = 'dashboard/views/project_selector.html'  # Add template name
    
    def get(self, request: HttpRequest, **kwargs: Any) -> TemplateResponse:
        """Handle project selection."""
        try:
            project_id = request.GET.get('project_id')
            if not project_id:
                return TemplateResponse(
                    request,
                    self.template_name,
                    {'error': 'No project selected'}
                )
                
            project = get_object_or_404(Project, id=project_id)
            mechanisms = (Obligation.objects
                        .filter(project=project)
                        .values('primary_environmental_mechanism')
                        .distinct())
            
            return TemplateResponse(request, self.template_name, {
                'project': project,
                'mechanisms': mechanisms
            })
            
        except Exception as e:
            logger.error(f"Project selection error: {str(e)}")
            return TemplateResponse(
                request,
                self.template_name,
                {'error': 'Error loading project data'}
            )

@method_decorator(login_required, name='dispatch')
class FilteredObligationsView(ListView):
    """Display filtered obligations."""
    template_name = 'dashboard/components/tables/obligation_list.html'
    context_object_name = 'obligations'
    
    def get_queryset(self) -> QuerySet[Obligation]:
        """Get filtered obligations."""
        project_id = self.kwargs.get('project_id')
        status = self.request.GET.get('status')
        
        queryset = Obligation.objects.filter(project_id=project_id)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset.order_by('action_due_date')
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add obligation list context."""
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('status')
        return context