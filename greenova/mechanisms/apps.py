"""App configuration for the mechanisms app.

Defines the MechanismsConfig class for Django app registry.
"""

from django.apps import AppConfig


class MechanismsConfig(AppConfig):
    """AppConfig for the mechanisms app."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "mechanisms"
