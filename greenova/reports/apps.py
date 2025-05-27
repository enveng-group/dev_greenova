"""apps.py for the reports app in Greenova."""

from django.apps import AppConfig


class ReportsConfig(AppConfig):
    """Application configuration for the Reports app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "reports"
    verbose_name = "Reports"
