from django.apps import AppConfig
from django.conf import settings


class ObligationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "obligations"
    verbose_name = "Environmental Obligations"

    def ready(self):
        """Initialize app and connect signals."""
        try:
            # Initialize app settings
            settings.OBLIGATIONS_SETTINGS = {
                'OVERDUE_WARNING_DAYS': 14,
                'CACHE_TIMEOUT': 3600,
                'ENABLE_NOTIFICATIONS': True,
                'AUDIT_CHANGES': True,
            }

            # Import and connect signals
            from . import signals

            signals.connect_signals()

            self.setup_logging()

        except Exception as e:
            import logging

            logger = logging.getLogger('greenova.obligations')
            logger.error(f'Failed to initialize Obligations app: {e}')

    def setup_logging(self):
        """Configure app-specific logging."""
        import logging
        import os
        from logging.handlers import RotatingFileHandler

        logger = logging.getLogger('greenova.obligations')
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            log_dir = os.path.join(settings.BASE_DIR, 'logs')
            os.makedirs(log_dir, exist_ok=True)

            file_handler = RotatingFileHandler(
                os.path.join(log_dir, 'obligations.log'),
                maxBytes=1024 * 1024,
                backupCount=5,
            )

            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(message)s'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
