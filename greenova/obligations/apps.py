from beartype import beartype  # Added for runtime type checking
from django.apps import AppConfig


class ObligationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "obligations"

    @beartype
    def ready(self) -> None:
        # Import signal handlers to ensure registration
        import obligations.signals  # noqa: F401
