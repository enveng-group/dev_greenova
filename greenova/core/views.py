"""Core views for the Greenova application."""
import logging
from typing import Any, Dict

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from django_htmx.http import HttpResponseClientRedirect, push_url, trigger_client_event

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
        return context
