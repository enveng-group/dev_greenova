from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"

    def ready(self) -> None:
        """Import signal handlers for the users app."""
        from . import signals  # noqa: F401
