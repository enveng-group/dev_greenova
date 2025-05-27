"""App configuration for the responsibility app.

Defines the ResponsibilityConfig class for Django app registry.
"""
from django.apps import AppConfig


class ResponsibilityConfig(AppConfig):
    """AppConfig for the responsibility app."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "responsibility"
