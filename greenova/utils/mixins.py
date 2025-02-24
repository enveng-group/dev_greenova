from typing import Any, Dict, Optional
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.views.generic.base import ContextMixin
from projects.models import Project
import logging
from django.urls import reverse
from .error_handlers import handle_error
from .messages import NO_DATA_AVAILABLE

logger = logging.getLogger(__name__)


class LoggedActionMixin(LoginRequiredMixin, View):
    """Mixin to add logging to view actions."""

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Log action and dispatch request."""
        logger.info(f"View action: {self.__class__.__name__} - User: {request.user}")
        return super().dispatch(request, *args, **kwargs)


class ProjectContextMixin(ContextMixin):
    """Mixin to add project-related context data."""

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Get project context data."""
        context = super().get_context_data(**kwargs)  # type: ignore
        try:
            project_id = self.request.GET.get('project_id')  # type: ignore
            if project_id:
                project = get_object_or_404(Project, id=project_id)
                context['project'] = project

                # Get unique mechanisms for this project
                mechanisms = (project.obligations
                              .values_list('primary_environmental_mechanism', flat=True)
                              .distinct()
                              .order_by('primary_environmental_mechanism'))

                context['mechanisms'] = mechanisms

        except Exception as e:
            logger.error(f"Error getting project context: {str(e)}")
            context['error'] = str(e)

        return context


class NavigationMixin:
    """Mixin to add consistent navigation context."""

    request: Optional[HttpRequest] = None

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add navigation context data."""
        context: Dict[str, Any] = super().get_context_data(**kwargs)  # type: ignore
        if self.request and self.request.user.is_authenticated:
            context['nav'] = self._get_navigation_items()
        return context

    def _get_navigation_items(self) -> Dict[str, str]:
        """Get navigation menu items."""
        return {
            'Dashboard': reverse('dashboard:home'),
            'Projects': reverse('projects:select'),
            'Profile': reverse('profiles:detail')
        }
