"""Admin configuration for the Greenova core app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from django.contrib import admin

from .forms import EnvironmentalObligationForm
from .models import EnvironmentalObligation


@admin.register(EnvironmentalObligation)
class EnvironmentalObligationAdmin(admin.ModelAdmin):  # type: ignore[misc]
    """Admin for EnvironmentalObligation with autocomplete support."""

    form = EnvironmentalObligationForm
    search_fields = ["name", "description"]
    list_display = ("name", "due_date", "is_complete")
    list_filter = ("is_complete", "due_date")
    # autocomplete_fields = ["project"]  # Example for large ForeignKey fields
