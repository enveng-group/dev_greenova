from django.apps import AppConfig


class CompanyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "company"
    verbose_name = "Companies"

    def ready(self) -> None:
        """Import signal handlers for the company app."""
        from . import signals  # noqa: F401
