"""Core app configuration."""
from django.apps import AppConfig
from django.contrib import admin

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Core System"

    def ready(self):
        """
        Initialize core components when Django is ready.
        """
        # Import signals to register handlers
        import core.signals

        # Customize admin site
        admin.site.site_header = "Environmental Obligations Management"
        admin.site.site_title = "Greenova Admin Portal"
        admin.site.index_title = "Welcome to Greenova Environmental Management"

        # Set site-wide settings
        admin.site.enable_nav_sidebar = True
