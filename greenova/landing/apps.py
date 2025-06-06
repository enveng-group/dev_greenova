"""App configuration for the Greenova landing app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from django.apps import AppConfig


class LandingConfig(AppConfig):
    """AppConfig for the landing page app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "landing"
