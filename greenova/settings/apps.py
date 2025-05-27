"""AppConfig for the settings app in Greenova.

Defines the Django application configuration for the settings app, which manages
project-wide and app-specific settings for the Greenova platform.
"""

from django.apps import AppConfig


class SettingsConfig(AppConfig):
    """App configuration for the Greenova settings app."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "settings"
    verbose_name = "Settings"
