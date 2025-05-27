"""App configuration for the Greenova dashboard app.

This module defines the DashboardConfig class for Django app registration.
"""

from django.apps import AppConfig


class DashboardConfig(AppConfig):
    """AppConfig for the dashboard app.

    Configures the dashboard application for Greenova, including default
    auto field and app name.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "dashboard"
