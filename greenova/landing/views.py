from typing import Any, Dict
from django.views.generic import TemplateView
from django.http import HttpRequest
import logging
from django.conf import settings

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
        # Add basic context data that was previously in utils
        context.update({
            'app_version': getattr(settings, 'APP_VERSION', '0.1.0'),
            'show_landing_content': True,
            'show_dashboard_link': self.request.user.is_authenticated
        })
        return context
