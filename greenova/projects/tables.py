# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Django-tables2 tables for the projects app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

import django_tables2 as tables

from .models import Project


class ProjectTable(tables.Table):
    """Table for listing Project instances."""

    name = tables.Column(linkify=True)
    description = tables.Column()
    created_at = tables.DateTimeColumn()
    updated_at = tables.DateTimeColumn()

    class Meta:
        model = Project
        template_name = "django_tables2/bootstrap5.html"
        fields = ("name", "description", "created_at", "updated_at")
