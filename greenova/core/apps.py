"""Core app configuration."""
from django.apps import AppConfig
from django.contrib import admin

class CoreConfig(AppConfig):
<<<<<<< HEAD
    """Configuration for the Core app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Core System'
=======
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Core System"
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

    def ready(self):
        """
        Initialize core components when Django is ready.
        """
        # Import signals to register handlers
        import core.signals

        # Customize admin site
<<<<<<< HEAD
        admin.site.site_header = 'Environmental Obligations Management'
        admin.site.site_title = 'Greenova Admin Portal'
        admin.site.index_title = 'Welcome to Greenova Environmental Management'
=======
        admin.site.site_header = "Environmental Obligations Management"
        admin.site.site_title = "Greenova Admin Portal"
        admin.site.index_title = "Welcome to Greenova Environmental Management"
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

        # Set site-wide settings
        admin.site.enable_nav_sidebar = True
