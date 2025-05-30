"""Copyright (C) 2025 Adrian Gallo.

This file is part of Greenova.

Greenova is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Greenova is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Greenova. If not, see <https://www.gnu.org/licenses/>.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

"""Views for the Greenova core app.

This module defines core views for routing, health checks, and system endpoints.
"""

from django.views.generic import TemplateView, View
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.conf import settings
from constants import AUTH_NAVIGATION, MAIN_NAVIGATION, USER_NAVIGATION
from typing import Any
import logging
import os


logger = logging.getLogger(__name__)


class HomeRouterView(View):
    """Route users to appropriate home page based on authentication status."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Route to landing page or dashboard."""
        if not request.user.is_authenticated:
            logger.debug("Unauthenticated user - redirecting to landing")
            return redirect("landing:home")

        logger.debug("Authenticated user - redirecting to dashboard")
        return redirect("dashboard:home")


class HealthCheckView(View):
    """Simple health check view for monitoring."""

    def get(self, request: HttpRequest) -> JsonResponse:  # pylint: disable=unused-argument
        """Return health status."""
        return JsonResponse(
            {
                "status": "ok",
                "version": getattr(settings, "APP_VERSION", "unknown"),
                "environment": getattr(settings, "ENVIRONMENT", "unknown"),
                "debug": settings.DEBUG,
            },
        )


class BaseTemplateView(TemplateView):
    """Base view with common template context."""

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        """Add common context data, including ts_available for TypeScript support."""
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "main_navigation": MAIN_NAVIGATION,
                "user_navigation": USER_NAVIGATION,
                "auth_navigation": AUTH_NAVIGATION,
                # Check if TypeScript is available (e.g., by checking if the file
                # exists)
                "ts_available": os.path.exists(
                    os.path.join(settings.STATIC_ROOT, "ts/dist/index.js"),
                ),
            },
        )
        return context
