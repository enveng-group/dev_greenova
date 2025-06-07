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

"""urls.py for the reports app in Greenova."""


from django.urls import path
from .views import ReportListView, export_all_reports, export_report, import_report

app_name = "reports"

urlpatterns = [
    path("", ReportListView.as_view(), name="report_list"),
    path("export/<int:report_id>/", export_report, name="export_report"),
    path("export-all/", export_all_reports, name="export_all_reports"),
    path("import/", import_report, name="import_report"),
]
