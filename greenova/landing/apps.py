"""App configuration for the landing app.

Defines the LandingConfig class for Django app registry.
"""

from django.apps import AppConfig


class LandingConfig(AppConfig):
    """AppConfig for the landing app."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "landing"
