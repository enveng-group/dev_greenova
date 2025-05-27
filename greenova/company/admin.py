"""
Admin configuration for the company app.

This module defines admin classes for managing company-related models in the
Django admin interface.
"""
from __future__ import annotations

import logging

from django.contrib import admin

from .models import Company

logger = logging.getLogger(__name__)

class BaseModelAdmin(admin.ModelAdmin):
    """Base admin class with type safety."""
    # ...existing code...

@admin.register(Company)
class CompanyAdmin(BaseModelAdmin):
    """Admin interface for the Company model.

    Provides list display, filtering, and search for company records in the admin site.
    """
    list_display = ("name", "company_type", "industry", "is_active", "created_at")
    list_filter = ("company_type", "is_active")
    search_fields = ("name",)
# ...existing code...
