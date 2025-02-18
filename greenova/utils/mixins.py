from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.views.generic import View
from django.db.models import QuerySet
from django.views.generic.detail import SingleObjectMixin
import logging  # Standard Python logging
from django.urls import reverse
from projects.models import Project  # Import the Project model

# Set up logger for this module
logger = logging.getLogger(__name__)

class LoggedActionMixin(LoginRequiredMixin, View):
    """Mixin to add logging to view actions."""
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.method:
            raise ValueError("Request method is required")
            
        action_name = f"{self.__class__.__name__}.{request.method.lower()}"
        logger.info(f"Starting {action_name}")
        try:
            response = super().dispatch(request, *args, **kwargs)
            logger.info(f"Completed {action_name}")
            return response
        except Exception as e:
            logger.error(f"Error in {action_name}: {str(e)}")
            raise

class ProjectContextMixin(SingleObjectMixin):
    """Mixin to add project-related context data."""
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            # Add common project data to context
            obj = getattr(self, 'object', None)
            if obj is not None and hasattr(obj, 'obligations'):
                context['project'] = obj
                obligations: QuerySet[Any] = obj.obligations.all()
                context['obligations'] = obligations
        except Exception as e:
            logger.error(f"Error getting project context: {str(e)}")
            raise
        return context

from django.views.generic.base import ContextMixin

class NavigationMixin(ContextMixin):
    """Mixin to add consistent navigation context."""
    
    request = None

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request:
            context.update({
                'is_authenticated': self.request.user.is_authenticated,
                'dashboard_url': reverse('dashboard:home'),
                'landing_url': reverse('landing:home'),
                'current_url': self.request.path,
            })
        return context

class ProjectDataMixin:
    """Mixin to handle common project data operations."""
    def get_project_analytics(self, project: Project) -> Dict[str, Any]:
        """Get analytics data for a project."""
        from utils.data_utils import AnalyticsDataProcessor
        processor = AnalyticsDataProcessor(project.obligations.all())
        return {
            'mechanism_data': processor.get_mechanism_data(mechanism="all"),  # Specify the mechanism parameter
            'completion_rate': self.calculate_completion_rate(project),
            'overdue_count': project.get_overdue_obligations().count()
        }
    
    def calculate_completion_rate(self, project: Project) -> float:
        """Calculate project completion rate."""
        total = project.obligations.count()
        if total == 0:
            return 0.0
        completed = project.get_completed_obligations().count()
        return (completed / total) * 100