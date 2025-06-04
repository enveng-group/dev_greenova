import logging
from typing import Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


@method_decorator(cache_control(max_age=300), name="dispatch")
class HomeView(TemplateView):
    """Landing page view."""

    template_name = "landing/index.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests."""
        logger.debug(
            "Landing page - User authenticated: %s",
            request.user.is_authenticated,
        )

        # Always render the full template
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add landing page context data."""
        context = super().get_context_data(**kwargs)
        # Add basic context data that was previously in utils
        context.update(
            {
                "app_version": getattr(settings, "APP_VERSION", "0.1.0"),
                "show_landing_content": True,
                "show_dashboard_link": self.request.user.is_authenticated,
            },
        )
        return context
