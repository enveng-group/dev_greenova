"""Table definition for EnvironmentalObligation using django-tables2.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

import django_tables2 as tables

from .models import EnvironmentalObligation


class EnvironmentalObligationTable(tables.Table):
    """Table for displaying EnvironmentalObligation objects."""

    class Meta:
        model = EnvironmentalObligation
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "name",
            "description",
            "due_date",
            "is_complete",
            "created_at",
            "updated_at",
        )
