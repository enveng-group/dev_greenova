import logging
from typing import Any, Dict

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, View

from .constants import AUTH_NAVIGATION, MAIN_NAVIGATION, USER_NAVIGATION

logger = logging.getLogger(__name__)

class HomeRouterView(View):
    """Route users to appropriate home page based on authentication status."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Route to landing page or dashboard."""
        if not request.user.is_authenticated:
            logger.debug("Unauthenticated user - redirecting to landing")
            return redirect('landing:home')

        logger.debug("Authenticated user - redirecting to dashboard")
        return redirect('dashboard:home')

class HealthCheckView(View):
    """Simple health check view for monitoring."""

    def get(self, request: HttpRequest) -> JsonResponse:  # pylint: disable=unused-argument
        """Return health status."""
        return JsonResponse({
            'status': 'ok',
            'version': getattr(settings, 'APP_VERSION', 'unknown'),
            'environment': getattr(settings, 'ENVIRONMENT', 'unknown'),
            'debug': settings.DEBUG,
        })

class BaseTemplateView(TemplateView):
    """Base view with common template context."""

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """Add common context data."""

        context = super().get_context_data(**kwargs)
        context.update({
            'main_navigation': MAIN_NAVIGATION,
            'user_navigation': USER_NAVIGATION,
            'auth_navigation': AUTH_NAVIGATION,
        })
        return context
