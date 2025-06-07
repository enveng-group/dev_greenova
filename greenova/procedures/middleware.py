"""Procedures middleware for chart data and state management.

This middleware handles chart data caching and state management for
procedures views, specifically for plotly integration.
"""

import logging
from collections.abc import Callable

from beartype import beartype
from django.http import HttpRequest, HttpResponse
from django.urls import resolve

logger = logging.getLogger(__name__)


class ProceduresChartMiddleware:
    """Middleware for managing chart data and state in procedures views.

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
            # Only process for procedures-related views
            if self._is_procedures_view(request):
                # Handle mechanism ID from URL parameters
                mechanism_id = request.GET.get("mechanism_id")
                if mechanism_id is not None:
                    request.session["selected_procedure_mechanism_id"] = mechanism_id
                    request.session.modified = True
                    logger.debug(
                        "Procedure mechanism ID set in session: %s",
                        mechanism_id,
                    )

                # Handle procedure name from URL parameters
                procedure_name = request.GET.get("procedure_name")
                if procedure_name is not None:
                    request.session["selected_procedure_name"] = procedure_name
                    request.session.modified = True
                    logger.debug("Procedure name set in session: %s", procedure_name)

                # Make session data available to templates
                if hasattr(request, "selected_procedure_mechanism_id"):
                    # Don't override if already set by a view
                    pass
                elif "selected_procedure_mechanism_id" in request.session:
                    request.selected_procedure_mechanism_id = request.session[
                        "selected_procedure_mechanism_id"
                    ]
                    logger.debug(
                        "Procedure mechanism ID retrieved from session: %s",
                        request.selected_procedure_mechanism_id,
                    )
                else:
                    request.selected_procedure_mechanism_id = None

                if hasattr(request, "selected_procedure_name"):
                    # Don't override if already set by a view
                    pass
                elif "selected_procedure_name" in request.session:
                    request.selected_procedure_name = request.session[
                        "selected_procedure_name"
                    ]
                    logger.debug(
                        "Procedure name retrieved from session: %s",
                        request.selected_procedure_name,
                    )
                else:
                    request.selected_procedure_name = None

                # Handle chart type preferences
                chart_type = request.GET.get("chart_type")
                if chart_type in {"svg", "interactive"}:
                    request.session["preferred_chart_type"] = chart_type
                    request.session.modified = True

                # Set default chart type if not specified
                if "preferred_chart_type" not in request.session:
                    request.session["preferred_chart_type"] = "svg"

                request.preferred_chart_type = request.session["preferred_chart_type"]

                # Handle filter preferences
                filter_params = {
                    "phase_filter": request.GET.get("phase_filter"),
                    "responsibility_filter": request.GET.get("responsibility_filter"),
                    "status_filter": request.GET.get("status_filter"),
                    "look_ahead": request.GET.get("look_ahead"),
                    "overdue_only": request.GET.get("overdue_only"),
                }

                # Store non-None filter values in session
                for key, value in filter_params.items():
                    if value is not None:
                        request.session[f"procedure_{key}"] = value
                        request.session.modified = True

        except Exception as e:
            logger.exception("Error in ProceduresChartMiddleware: %s", str(e))

    @beartype
    def process_response(self, request: HttpRequest, response: HttpResponse) -> None:
        """Process the response after the view has been called.

        Args:
            request: The HTTP request object.
            response: The HTTP response object.

        """
        # Add cache headers for chart data
        if self._is_procedures_view(request) and response.status_code == 200:
            response["Cache-Control"] = "public, max-age=300"  # 5 minutes
            response["Vary"] = "Accept, HX-Request"

    @beartype
    def _is_procedures_view(self, request: HttpRequest) -> bool:
        """Check if the current request is for a procedures view.

        Args:
            request: The HTTP request object.

        Returns:
            True if the request is for a procedures view, False otherwise.

        """
        try:
            resolver_match = resolve(request.path)
            return resolver_match.app_name == "procedures"
        except Exception:
            return False
