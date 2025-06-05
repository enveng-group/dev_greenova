# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Core views for the Greenova application.

This module provides the main views for the Greenova core app, including the
landing page and shared context logic.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Logging for diagnostics and debugging

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging
from typing import Any

from beartype import beartype
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from .types import (
    HttpRequest as GreenovaHttpRequest,
    QuerySet,
    StatusData,
    DjangoError,
    ModelOperationError,
    ChoicesType,
)

logger = logging.getLogger(__name__)


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class HomeView(TemplateView):
    """Landing page view."""

    template_name = "landing/index.html"

    @beartype
    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse:
        """Handle GET requests.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The rendered landing page.
        """
        logger.debug(
            "Landing page access - User authenticated: %s",
            request.user.is_authenticated,
        )
        return super().get(request, *args, **kwargs)

    @beartype
    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add landing page context data.

        Args:
            **kwargs: Additional context keyword arguments.

        Returns:
            dict[str, Any]: The context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context["user_authenticated"] = self.request.user.is_authenticated
        return context
