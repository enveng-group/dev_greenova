"""Core views for the Greenova application."""

import logging
from typing import Any

from beartype import beartype
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class HomeView(TemplateView):
    """Landing page view."""

    template_name = "landing/index.html"

    @beartype
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests."""
        logger.debug(
            "Landing page access - User authenticated: %s",
            request.user.is_authenticated,
        )

        return super().get(request, *args, **kwargs)

    @beartype
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add landing page context data."""
        context = super().get_context_data(**kwargs)
        # Add basic context data
        context["user_authenticated"] = self.request.user.is_authenticated
        return context
