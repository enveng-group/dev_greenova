import logging
from typing import Any, Dict, List, Sequence, TypeVar, cast

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from django_htmx.http import (HttpResponseClientRedirect, HttpResponseClientRefresh,
                              push_url, trigger_client_event)
from obligations.models import Obligation

from .models import Project

User = get_user_model()
logger = logging.getLogger(__name__)

T = TypeVar('T')

@method_decorator(cache_control(max_age=300), name='dispatch')
@method_decorator(vary_on_headers('HX-Request'), name='dispatch')
class ProjectSelectionView(LoginRequiredMixin, TemplateView):
    """Handle project selection."""
    template_name = 'projects/projects_selector.html'

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

    def requires_special_access(self, project_id: str, user: AbstractUser) -> bool:
        """Check if a project requires special access permissions."""
        try:
            project = Project.objects.get(id=project_id)
            # Implement your permission logic here
            return False  # Return True if special access is required
        except Project.DoesNotExist:
            logger.warning(f'Project {project_id} not found during permission check')
            return False

def project_obligations(request, project_id):
    def project_obligations(request: HttpRequest, project_id: str) -> JsonResponse:
        """ Retrieve obligations associated with a specific project. """
        project = get_object_or_404(Project, id=project_id)
        obligations = Obligation.objects.filter(project=project)

        # Serialize obligations
        obligations_data = [{'id': o.id, 'obligation_number': o.obligation_number} for o in obligations]

        return JsonResponse({'obligations': obligations_data})
    """ Retrieve obligations associated with a specific project. """
    project = get_object_or_404(Project, id=project_id)
    obligations = Obligation.objects.filter(project=project)

    # Serialize obligations
    obligations_data = [{'id': o.id, 'obligation_number': o.obligation_number} for o in obligations]

    return obligations_data
