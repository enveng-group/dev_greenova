# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Dashboard middleware for maintaining state between requests.

This middleware ensures project selection persists across requests and
handles the injection of necessary context for dashboard rendering.
"""

import logging
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse
from django.urls import resolve

logger = logging.getLogger(__name__)


class DashboardPersistenceMiddleware:
    """Middleware for maintaining dashboard state across requests.

    This middleware:
    1. Preserves project selection across requests
    2. Ensures consistent URL parameters for dashboard views
    3. Adds required context for dashboard components
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize the middleware.

        Args:
            get_response: The callable that processes the request and returns the response

        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process the request through the middleware.

        Args:
            request: The HTTP request object

        Returns:
            The HTTP response object

        """
        # Before the view is called
        self.process_request(request)

        # Call the next middleware or view
        response = self.get_response(request)

        # After the view is called
        self.process_response(request, response)

        return response

    def process_request(self, request: HttpRequest) -> None:
        """Process the request before it reaches the view.

        Args:
            request: The HTTP request object

        """
        try:
            # Only process for dashboard-related views
            if self._is_dashboard_view(request):
                # If project_id is in the request, update the session
                project_id = request.GET.get("project_id")
                if project_id is not None:  # Allow empty string
                    request.session["selected_project_id"] = project_id
                    request.session.modified = True
                    logger.debug("Project ID set in session: %s", project_id)

                # Make selected_project_id available to templates
                if hasattr(request, "selected_project_id"):
                    # Don't override if already set by a view
                    pass
                elif "selected_project_id" in request.session:
                    request.selected_project_id = request.session["selected_project_id"]
                    logger.debug(
                        "Project ID retrieved from session: %s",
                        request.selected_project_id,
                    )
                else:
                    request.selected_project_id = None
        except Exception as e:
            logger.exception("Error in DashboardPersistenceMiddleware: %s", str(e))

    def process_response(self, request: HttpRequest, response: HttpResponse) -> None:
        """Process the response after the view has been called.

        Args:
            request: The HTTP request object
            response: The HTTP response object

        """
        # This method could be used to modify the response if needed

    def _is_dashboard_view(self, request: HttpRequest) -> bool:
        """Check if the current request is for a dashboard view.

        Args:
            request: The HTTP request object

        Returns:
            True if the request is for a dashboard view, False otherwise

        """
        try:
            resolver_match = resolve(request.path)
            return resolver_match.app_name == "dashboard"
        except BaseException:
            return False
