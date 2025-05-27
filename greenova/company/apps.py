"""
App configuration for the company app.

Defines the Django AppConfig for the company application,
which manages company-related features and initialization.
"""
from django.apps import AppConfig


class CompanyConfig(AppConfig):
    """Configuration for the company app."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "company"
    verbose_name = "Companies"
