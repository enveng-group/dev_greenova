# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Common utilities for the Greenova core app.

This module provides shared utility functions for namespace resolution,
user display name formatting, and application settings retrieval.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Logging for error handling and diagnostics

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging
from typing import Any

from beartype import beartype
from django.conf import settings
from django.http import HttpRequest

logger = logging.getLogger(__name__)


@beartype
def get_active_namespace(request: HttpRequest) -> str:
    """Get the active namespace from the request.

    Args:
        request: The current HttpRequest object.

    Returns:
        The namespace string if found, otherwise an empty string.
    """
    try:
        if hasattr(request, "resolver_match") and request.resolver_match:
            return request.resolver_match.namespace or ""
    except AttributeError as e:
        logger.exception("Error getting namespace: %s", str(e))
    return ""


@beartype
def get_user_display_name(user: Any) -> str:
    """Get the best display name for a user.

    Args:
        user: The user object.

    Returns:
        The user's display name as a string.
    """
    if hasattr(user, "get_full_name") and callable(user.get_full_name):
        full_name = user.get_full_name()
        if full_name:
            return full_name

    return user.username if hasattr(user, "username") else str(user)


@beartype
def get_app_settings() -> dict[str, Any]:
    """Get application settings for templates.

    Returns:
        A dictionary of application settings.
    """
    return {
        "APP_VERSION": getattr(settings, "APP_VERSION", "dev"),
        "DEBUG": getattr(settings, "DEBUG", False),
        "SITE_NAME": getattr(settings, "SITE_NAME", "Greenova"),
        "SITE_DESCRIPTION": getattr(
            settings,
            "SITE_DESCRIPTION",
            "Environmental Compliance Management System",
        ),
    }
