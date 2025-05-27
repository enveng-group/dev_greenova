"""App configuration for the obligations app.

Defines the ObligationsConfig class for Django app registry.
"""
from django.apps import AppConfig


class ObligationsConfig(AppConfig):
    """AppConfig for the obligations app."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "obligations"
