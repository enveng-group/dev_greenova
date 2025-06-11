# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Authentication middleware for handling login redirects with project selection.

This middleware ensures that after login, users are redirected to the dashboard
with a project automatically selected if they have access to projects.
"""

import logging
from collections.abc import Callable

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.http import HttpRequest, HttpResponse
from projects.models import Project

logger = logging.getLogger(__name__)


class LoginRedirectMiddleware:
    """Middleware to handle login redirects with automatic project selection.

    This middleware works in conjunction with the user_logged_in signal
    to ensure users are redirected to the dashboard with a project selected.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize the middleware.

        Args:
            get_response: The next middleware/view in the chain

        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process the request through the middleware.

        Args:
            request: The incoming HTTP request

        Returns:
            HttpResponse: The response from the next middleware/view

        """
        return self.get_response(request)


@receiver(user_logged_in)
def handle_login_redirect(sender, user, request, **kwargs) -> None:
    """Handle user login and ensure proper dashboard setup.

    This signal handler:
    1. Automatically selects the user's first project
    2. Ensures the session is properly configured
    3. Forces a full page reload to the dashboard

    Args:
        sender: The sender of the signal
        user: The user who just logged in
        request: The current HTTP request
        **kwargs: Additional keyword arguments

    """
    if not request:
        return

    try:
        # Get the user's first project
        first_project = Project.objects.filter(members=user).first()

        if first_project:
            # Set the project in the session
            request.session["selected_project_id"] = str(first_project.pk)
            request.session.modified = True
            logger.info(
                "Auto-selected project %s (%s) for user %s after login",
                first_project.name,
                first_project.pk,
                user.username,
            )
        else:
            # Clear any existing project selection
            request.session.pop("selected_project_id", None)
            logger.info("No projects available for user %s", user.username)

        # Mark that we need a full page reload
        request.session["_force_dashboard_reload"] = True

    except Exception as e:
        logger.exception("Error in login redirect handler: %s", str(e))
