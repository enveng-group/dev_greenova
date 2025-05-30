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

"""Authentication app configuration module.

This module defines the Django AppConfig for the authentication application,
which handles user authentication, registration, and related functionality.
"""


from django.apps import AppConfig
class AuthenticationConfig(AppConfig):
    """Configuration for the authentication app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"
    verbose_name = "Authentication"

    def ready(self) -> None:
        """Initialize app when Django starts.

        Import signals or perform other initialization here.
        """
        # Import signals or perform other initialization if needed

    def get_app_name(self) -> str:
        """Return the name of this app.

        Returns:
            str: The name of the authentication app.

        """
        return self.name
