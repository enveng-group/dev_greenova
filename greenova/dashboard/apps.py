"""Copyright (C) 2024 Adrian Gallo <agallo@enveng-group.com.au>
This file is part of Greenova and is licensed under the AGPL-3.0.

Dashboard app configuration for Greenova.
"""

from beartype import beartype
from django.apps import AppConfig


@beartype
class DashboardConfig(AppConfig):
    """AppConfig for the dashboard app."""

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "dashboard"
