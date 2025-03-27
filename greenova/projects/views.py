import logging
from typing import Any, Callable, Dict, TypeVar, cast

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView

from django_htmx.http import HttpResponseClientRedirect, trigger_client_event

from .models import Project

User = get_user_model()
logger = logging.getLogger(__name__)

T = TypeVar('T')
# Type ignore for method_decorator and vary_on_headers due to django-stubs limitations
@method_decorator(cache_control(max_age=300), name='dispatch')  # type: ignore
@method_decorator(vary_on_headers('HX-Request'), name='dispatch')  # type: ignore
class ProjectSelectionView(LoginRequiredMixin, TemplateView):
    """Handle project selection."""
    template_name = 'projects/projects_selector.html'
    login_url = 'account_login'  # Updated to use allauth's login URL name
    redirect_field_name = 'next'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests for project selection."""
        response = super().get(request, *args, **kwargs)

        # If htmx request, add appropriate triggers and handle client-side updates
        if request.htmx:
            # Trigger a client event to refresh any project-dependent elements
            trigger_client_event(response, 'projectSelected')

            # If the user is selecting a project that requires special permissions
            project_id = request.GET.get('project_id')
            if project_id and self.requires_special_access(project_id, request.user):
                return HttpResponseClientRedirect('/permissions-check/')

        return response

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Get context data for project selection."""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get user's projects
        projects = Project.objects.filter(memberships__user=user).distinct()
        context['projects'] = projects

        # Get selected project ID from query parameters
        selected_project_id = self.request.GET.get('project_id')
        context['selected_project_id'] = selected_project_id

        return context

    def requires_special_access(self, project_id: str, user: AbstractUser) -> bool:
        """Check if a project requires special access permissions."""
        try:
            project = Project.objects.get(id=project_id)
            # Implement your permission logic here
            return False  # Return True if special access is required
        except Project.DoesNotExist:
            logger.warning(f'Project {project_id} not found during permission check')
            return False
