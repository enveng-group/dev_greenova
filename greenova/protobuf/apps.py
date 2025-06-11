"""Django app configuration for Protobuf integration."""

from django.apps import AppConfig


class ProtobufConfig(AppConfig):
    """Configuration for the Protobuf Django app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "protobuf"
    verbose_name = "Protobuf Integration"

    def ready(self) -> None:
        """Initialize the app when Django starts."""
        # Import any signals or initialization code here
