from beartype import beartype  # Added for runtime type checking
from django.apps import AppConfig


class AuditingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auditing"

    @beartype
    def ready(self) -> None:
        # Import signal handlers to ensure registration
        import auditing.signals  # noqa: F401
