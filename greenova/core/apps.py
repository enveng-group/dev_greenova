from django.apps import AppConfig
from django.contrib import admin


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        """
        Configure admin site settings when Django is ready.
        This ensures the app registry is fully loaded.
        """
        # Customize admin site
        admin.site.site_header = "Environmental Obligations Management"
        admin.site.site_title = "Enssol Admin Portal"
        admin.site.index_title = "Welcome to Enssol Environmental Obligations Management"
