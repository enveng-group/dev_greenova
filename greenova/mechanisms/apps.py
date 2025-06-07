"""AppConfig for the mechanisms app.

This module defines the Django application configuration for the mechanisms
app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import logging

from beartype import beartype
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class MechanismsConfig(AppConfig):
    """Django AppConfig for the mechanisms app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "mechanisms"

    @beartype
    def ready(self) -> None:
        """Perform app-specific initialization when the app is ready."""
