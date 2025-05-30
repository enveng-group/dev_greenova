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

"""Core app configuration."""

from django.apps import AppConfig
from django.contrib import admin


class CoreConfig(AppConfig):
    """AppConfig for the core system of Greenova.

    Handles core app configuration and admin customization for the project.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Core System"

    def ready(self) -> None:
        """Initialize core components when Django is ready."""
        # Customize admin site
        admin.site.site_header = "Environmental Obligations Management"
        admin.site.site_title = "Greenova Admin Portal"
        admin.site.index_title = "Welcome to Greenova Environmental Management"

        # Set site-wide settings
        admin.site.enable_nav_sidebar = True
