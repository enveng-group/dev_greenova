"""App configuration for the procedures app.

Defines the ProceduresConfig class for Django app registry.
"""
from django.apps import AppConfig


class ProceduresConfig(AppConfig):
    """AppConfig for the procedures app."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "procedures"
