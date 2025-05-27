"""App configuration for the projects app.

Defines the ProjectsConfig class for Django app registry.
"""
from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    """AppConfig for the projects app."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "projects"
