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

"""Admin configuration for the responsibility app.

This module registers the Responsibility and ResponsibilityAssignment models
and customizes their admin interface.
"""


from django.contrib import admin
from .models import Responsibility, ResponsibilityAssignment


@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    """Admin configuration for Responsibility model."""

    list_display = ("name", "description")
    search_fields = ("name", "description")


@admin.register(ResponsibilityAssignment)
class ResponsibilityAssignmentAdmin(admin.ModelAdmin):
    """Admin configuration for ResponsibilityAssignment model."""

    list_display = ("user", "obligation", "role", "created_by", "created_at")
    list_filter = ("role", "created_at")
    search_fields = ("user__username", "user__email", "obligation__obligation_number")
    raw_id_fields = ("user", "obligation", "role", "created_by")
