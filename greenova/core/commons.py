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

"""Common utility functions for the Greenova core app.

This module provides shared helpers for request handling, user display,
and other core utilities.
"""

from django.http import HttpRequest
from django.conf import settings
import logging
from typing import Any


logger = logging.getLogger(__name__)


def get_active_namespace(request: HttpRequest) -> str:
    """Get the active namespace from the request.

    Args:
        request: The HTTP request object.

    Returns:
        The namespace string if available, otherwise an empty string.

    """
    try:
        if hasattr(request, "resolver_match") and request.resolver_match:
            return request.resolver_match.namespace or ""
    except AttributeError:
        logger.exception("Error getting namespace")
    return ""


def get_user_display_name(user: object) -> str:
    """Get the best display name for a user.

    Args:
        user: The user object to get the display name for.

    Returns:
        The user's full name if available, otherwise the username or string
        representation.

    """
    if hasattr(user, "get_full_name") and callable(user.get_full_name):
        full_name = user.get_full_name()
        if full_name:
            return str(full_name)

    return user.username if hasattr(user, "username") else str(user)


def get_app_settings() -> dict[str, Any]:
    """Get application settings for templates.

    Returns:
        A dictionary containing application settings for use in templates.

    """
    return {
        "APP_VERSION": getattr(settings, "APP_VERSION", "dev"),
        "DEBUG": getattr(settings, "DEBUG", False),
        "SITE_NAME": getattr(settings, "SITE_NAME", "Greenova"),
        "SITE_DESCRIPTION": getattr(
            settings, "SITE_DESCRIPTION", "Environmental Compliance Management System",
        ),
    }
