import logging
from typing import Any, Dict, TypedDict, cast

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from django_htmx.http import HttpResponseClientRedirect, push_url, trigger_client_event

logger = logging.getLogger(__name__)

# Type definition for django-htmx request attribute
class HtmxDetails(TypedDict, total=False):
    """Type hints for django-htmx request.htmx attributes."""
    boosted: bool
    current_url: str
    history_restore_request: bool
    prompt: str
    target: str
    trigger: str
    trigger_name: str

@method_decorator(cache_control(max_age=300), name='dispatch')
@method_decorator(vary_on_headers("HX-Request"), name='dispatch')
class HomeView(TemplateView):
    """Landing page view."""
    template_name = 'landing/index.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests."""
        logger.debug(
            "Landing page - User authenticated: %s", request.user.is_authenticated)

        response = super().get(request, *args, **kwargs)

        # If htmx request, handle proper URL management
        if hasattr(request, 'htmx'):
            # Cast request.htmx to our type definition for mypy
            htmx = cast(HtmxDetails, request.htmx)

            # Push the URL to the browser history to ensure proper navigation
            push_url(response, request.path)

            # Trigger animations or other client-side effects if needed
            trigger_client_event(response, 'landingLoaded')

            # If user is authenticated and accessing the landing page directly,
            # we might want to redirect them to the dashboard
            if request.user.is_authenticated and htmx.get('boosted', False):
                return HttpResponseClientRedirect('/dashboard/')

        return response

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add landing page context data."""
        context = super().get_context_data(**kwargs)
        # Add basic context data that was previously in utils
        context.update({
            'app_version': getattr(settings, 'APP_VERSION', '0.1.0'),
            'show_landing_content': True,
            'show_dashboard_link': self.request.user.is_authenticated
        })
        return context
