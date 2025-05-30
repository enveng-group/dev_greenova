"""Copyright (C) 2025 Adrian Gallo.

This file is part of Greenova.

Greenova is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Greenova is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Greenova. If not, see <https://www.gnu.org/licenses/>.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

"""Admin configuration for the company app.

This module defines admin classes for managing company-related models in the
Django admin interface.
"""


from __future__ import annotations
import logging

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
