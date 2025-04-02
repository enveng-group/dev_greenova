from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """Configuration for the authentication app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
    verbose_name = 'Authentication'

    def ready(self):
        """
        Initialize app when Django starts.
        Import signals or perform other initialization here.
        """
        # Import signals or perform other initialization if needed
