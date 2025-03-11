from typing import Dict, Any, cast, TypeVar, List, Sequence
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django_htmx.http import (
    HttpResponseClientRedirect,
    HttpResponseClientRefresh,
    trigger_client_event,
    push_url
)
from .models import Project
from obligations.models import Obligation
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

T = TypeVar('T')

@method_decorator(cache_control(max_age=300), name='dispatch')
@method_decorator(vary_on_headers("HX-Request"), name='dispatch')
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
            logger.warning(f"Project {project_id} not found during permission check")
            return False
