from typing import Any, Dict, Optional
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.views.generic import View
import logging
from django.urls import reverse
from projects.models import Project
from django.views.generic.base import ContextMixin
from .error_handlers import handle_dashboard_error
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

    @handle_dashboard_error
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add project context data with error handling."""
        context = super().get_context_data(**kwargs)
        try:
            project = self.get_object()
            if isinstance(project, Project):
                context['project'] = project
            else:
                context['message'] = NO_DATA_AVAILABLE
        except Exception as e:
            logger.error(f"Error getting project context: {e}")
            raise
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
