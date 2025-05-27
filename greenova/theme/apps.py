"""AppConfig for the theme app in Greenova.

Defines the Django application configuration for the theme app, which manages
theming and appearance for the Greenova platform.
"""

from django.apps import AppConfig


class ThemeConfig(AppConfig):
    """App configuration for the Greenova theme app."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "theme"
