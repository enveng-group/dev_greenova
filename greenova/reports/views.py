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

"""views.py for the reports app in Greenova."""

from django.db.models import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Report
from guardian.shortcuts import get_objects_for_user


class ReportListView(LoginRequiredMixin, ListView):
    """List all reports with object-level permission checks."""

    model = Report
    template_name = "reports/reports_list.html"
    context_object_name = "reports"

    def get_queryset(self) -> QuerySet:
        """Return the queryset of all reports the user has permission to view."""
        return get_objects_for_user(
            self.request.user,
            "reports.view_report",
            Report.objects.all(),
        )
