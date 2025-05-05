# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: 	AGPL-3.0-or-later

"""
Authentication app configuration module.

This module defines the Django AppConfig for the authentication application,
which handles user authentication, registration, and related functionality.
"""

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """Configuration for the authentication app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
    verbose_name = 'Authentication'

    def ready(self):
        """
        Initialize app when Django starts.
        Import signals or perform other initialization here.
        """
        # Import signals or perform other initialization if needed

    def get_app_name(self):
        """
        Return the name of this app.

        Returns:
            str: The name of the authentication app.
        """
        return self.name
