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

"""Custom template tags for the Greenova core app.

This module defines reusable Django template tags for navigation, theming,
and user display.
"""


from commons import get_active_namespace, get_user_display_name
import logging
from constants import (
    AUTH_NAVIGATION,
    MAIN_NAVIGATION,
    THEME_OPTIONS,
    USER_NAVIGATION,
)
from django import template
from django.urls import NoReverseMatch, reverse
from django.conf import settings

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(context: Any, url_name: Any, css_class: str = "active") -> str:
    """Return css_class if the current URL matches the given URL name."""
    request = context.get("request")
    if not request:
        return ""

    try:
        current_url = request.path
        target_url = reverse(url_name)
        if current_url.startswith(target_url):
            return css_class
    except NoReverseMatch:
        logger.debug("No reverse match for %s", url_name)
    return ""


@register.inclusion_tag("core/components/breadcrumbs.html", takes_context=True)
def breadcrumb_navigation(context: Any) -> dict:
    """Render breadcrumb navigation based on request path."""
    request = context.get("request")
    if not request:
        return {"crumbs": []}

    # Build breadcrumbs based on namespace and url name
    crumbs = []

    # Always include home
    crumbs.append(
        {
            "title": "Home",
            "url": reverse("home"),
            "active": request.path == reverse("home"),
        },
    )

    # Add namespace-based breadcrumb if applicable
    namespace = get_active_namespace(request)
    if namespace and namespace != "home":
        try:
            url = reverse(f"{namespace}:home")
            crumbs.append(
                {
                    "title": namespace.title(),
                    "url": url,
                    "active": request.path == url,
                },
            )
        except NoReverseMatch:
            # Try with just the namespace
            try:
                url = reverse(namespace)
                crumbs.append(
                    {
                        "title": namespace.title(),
                        "url": url,
                        "active": request.path == url,
                    },
                )
            except NoReverseMatch:
                # Just add the namespace as text
                crumbs.append(
                    {
                        "title": namespace.title(),
                        "url": None,
                        "active": True,
                    },
                )

    return {"crumbs": crumbs}


@register.inclusion_tag("core/components/auth_menu.html", takes_context=True)
def auth_menu(context: Any) -> dict:
    """Render authentication menu based on user status."""
    request = context.get("request")
    user = request.user if request else None

    return {
        "user": user,
        "is_authenticated": user.is_authenticated if user else False,
        "user_navigation": USER_NAVIGATION,
        "auth_navigation": AUTH_NAVIGATION,
        "user_display_name": get_user_display_name(user)
        if user and user.is_authenticated
        else None,
    }


@register.inclusion_tag("core/components/theme_switcher.html")
def theme_switcher() -> dict:
    """Render theme switcher component."""
    return {
        "theme_options": THEME_OPTIONS,
    }


@register.simple_tag
def site_version() -> str:
    """Return the current site version."""
    return getattr(settings, "APP_VERSION", "dev")


@register.inclusion_tag("core/components/main_navigation.html", takes_context=True)
def main_navigation(context: Any) -> dict:
    """Render the main navigation menu."""
    request = context.get("request")
    current_namespace = get_active_namespace(request) if request else ""

    return {
        "navigation_items": MAIN_NAVIGATION,
        "current_namespace": current_namespace,
    }


@register.filter
def user_role_in_project(project: Any, user: Any) -> str:
    """Get user's role in a project."""
    if hasattr(project, "get_user_role"):
        return project.get_user_role(user)
    return None


@register.simple_tag(takes_context=True)
def base_url(context: Any) -> str:
    """Get the base URL from the request."""
    request = context.get("request")
    if request:
        return f"{request.scheme}://{request.get_host()}"
    return ""


@register.filter(name="format_date")
def format_date(date_value: Any, format_string: str = "%d %b %Y") -> str:
    """Format a date with a specified format string."""
    if date_value is None:
        return ""
    try:
        return date_value.strftime(format_string)
    except (AttributeError, ValueError):
        return str(date_value)
