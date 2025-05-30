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

"""Jinja2 environment configuration for Greenova.

This module customizes the Jinja2 environment for Django templates in Greenova.
"""

# Import your custom filters and globals
from django.contrib.staticfiles.storage import staticfiles_storage
from django.middleware.csrf import get_token
from django.urls import reverse
from django.utils import translation
from django_htmx.jinja import django_htmx_script
from django_hyperscript.templatetags.hyperscript import hs_dump
from jinja2 import Environment


def environment(**options: object) -> Environment:
    """Create a custom Jinja2 environment with Django-specific filters and globals."""
    # Filter out Django-specific options that Jinja2 doesn't understand
    jinja2_options = {k: v for k, v in options.items() if k != "debug"}

    # Set autoescape=True if it's not already specified in options
    if "autoescape" not in jinja2_options:
        jinja2_options["autoescape"] = True

    # Create environment with filtered options - adding a nosec to satisfy Bandit
    # autoescape is set in jinja2_options above
    env = Environment(**jinja2_options)  # nosec B701
    env.globals["static"] = staticfiles_storage.url
    env.globals["url"] = reverse
    env.globals["get_current_language"] = translation.get_language
    env.globals["csrf_token"] = get_token  # Add CSRF token support
    env.globals["django_htmx_script"] = django_htmx_script  # Add django_htmx support
    env.globals["hyperscript"] = hs_dump  # Using hs_dump instead of hyperscript_widget

    return env
