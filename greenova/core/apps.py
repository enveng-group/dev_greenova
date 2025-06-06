"""App configuration for the Greenova core app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """AppConfig for the core app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Core"


app_name = "core"
