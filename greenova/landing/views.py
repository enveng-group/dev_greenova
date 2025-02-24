from typing import Any, Dict
from django.views.generic import TemplateView
from django.http import HttpRequest
import logging
from utils.context_processors import greenova_context

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    """Landing page view."""
    template_name = 'landing/index.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        """Handle GET requests."""
        logger.debug(
            f"Landing page access - User authenticated: {request.user.is_authenticated}")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add landing page context data."""
        context = super().get_context_data(**kwargs)
        context.update(greenova_context(self.request))
        # Add show_landing_content flag
        context['show_landing_content'] = True
        # Add dashboard link if authenticated
        if self.request.user.is_authenticated:
            context['show_dashboard_link'] = True

        return context
