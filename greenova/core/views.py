<<<<<<< HEAD
"""Core views for the Greenova application."""
import logging
from typing import Any, Dict

from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from django_htmx.http import push_url

logger = logging.getLogger(__name__)


@method_decorator(cache_control(max_age=300), name='dispatch')
@method_decorator(vary_on_headers('HX-Request'), name='dispatch')
class HomeView(TemplateView):
    """Landing page view."""

    template_name = 'landing/index.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests."""
        logger.debug(
            f'Landing page access - User authenticated: {request.user.is_authenticated}'
        )

        response = super().get(request, *args, **kwargs)

        # If htmx request, handle proper URL management
        if request.htmx:
            push_url(response, request.path)

        return response

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add landing page context data."""
        context = super().get_context_data(**kwargs)
        # Add basic context data
        context['user_authenticated'] = self.request.user.is_authenticated
=======
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse
from typing import Dict, Any
import logging

from .mixins import ViewMixin, AuthViewMixin

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

    def get(self, request: HttpRequest) -> JsonResponse:
        """Return health status."""
        from django.conf import settings

        return JsonResponse({
            'status': 'ok',
            'version': getattr(settings, 'APP_VERSION', 'unknown'),
            'environment': getattr(settings, 'ENVIRONMENT', 'unknown'),
            'debug': settings.DEBUG,
        })

class BaseTemplateView(ViewMixin, TemplateView):
    """Base view with common template context."""

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """Add common context data."""
        from .constants import MAIN_NAVIGATION, USER_NAVIGATION, AUTH_NAVIGATION

        context = super().get_context_data(**kwargs)
        context.update({
            'main_navigation': MAIN_NAVIGATION,
            'user_navigation': USER_NAVIGATION,
            'auth_navigation': AUTH_NAVIGATION,
        })
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
        return context
