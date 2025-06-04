"""Mechanisms middleware for chart data and state management.

This middleware handles chart data caching and state management for
mechanisms views, specifically for plotly integration.
"""

import logging
from collections.abc import Callable

from beartype import beartype
from django.http import HttpRequest, HttpResponse
from django.urls import resolve

logger = logging.getLogger(__name__)


class MechanismsChartMiddleware:
    """Middleware for managing chart data and state in mechanisms views.

    This middleware:
    1. Caches chart data for performance
    2. Manages chart state across requests
    3. Provides plotly integration support
    """

    @beartype
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize the middleware.

        Args:
            get_response: The callable that processes the request and returns the response.

        """
        self.get_response = get_response

    @beartype
    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process the request through the middleware.

        Args:
            request: The HTTP request object.

        Returns:
            The HTTP response object.

        """
        # Before the view is called
        self.process_request(request)

        # Call the next middleware or view
        response = self.get_response(request)

        # After the view is called
        self.process_response(request, response)

        return response

    @beartype
    def process_request(self, request: HttpRequest) -> None:
        """Process the request before it reaches the view.

        Args:
            request: The HTTP request object.

        """
        try:
            # Only process for mechanisms-related views
            if self._is_mechanisms_view(request):
                # Handle mechanism ID from URL parameters
                mechanism_id = request.GET.get("mechanism_id")
                if mechanism_id is not None:
                    request.session["selected_mechanism_id"] = mechanism_id
                    request.session.modified = True
                    logger.debug("Mechanism ID set in session: %s", mechanism_id)

                # Make selected_mechanism_id available to templates
                if hasattr(request, "selected_mechanism_id"):
                    # Don't override if already set by a view
                    pass
                elif "selected_mechanism_id" in request.session:
                    request.selected_mechanism_id = request.session[
                        "selected_mechanism_id"
                    ]
                    logger.debug(
                        "Mechanism ID retrieved from session: %s",
                        request.selected_mechanism_id,
                    )
                else:
                    request.selected_mechanism_id = None

                # Handle chart type preferences
                chart_type = request.GET.get("chart_type")
                if chart_type in {"svg", "interactive"}:
                    request.session["preferred_chart_type"] = chart_type
                    request.session.modified = True

                # Set default chart type if not specified
                if "preferred_chart_type" not in request.session:
                    request.session["preferred_chart_type"] = "svg"

                request.preferred_chart_type = request.session["preferred_chart_type"]

        except Exception as e:
            logger.exception("Error in MechanismsChartMiddleware: %s", str(e))

    @beartype
    def process_response(self, request: HttpRequest, response: HttpResponse) -> None:
        """Process the response after the view has been called.

        Args:
            request: The HTTP request object.
            response: The HTTP response object.

        """
        # Add cache headers for chart data
        if self._is_mechanisms_view(request) and response.status_code == 200:
            response["Cache-Control"] = "public, max-age=300"  # 5 minutes
            response["Vary"] = "Accept, HX-Request"

    @beartype
    def _is_mechanisms_view(self, request: HttpRequest) -> bool:
        """Check if the current request is for a mechanisms view.

        Args:
            request: The HTTP request object.

        Returns:
            True if the request is for a mechanisms view, False otherwise.

        """
        try:
            resolver_match = resolve(request.path)
            return resolver_match.app_name == "mechanisms"
        except Exception:
            return False
