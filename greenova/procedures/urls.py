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

"""URL configuration for the procedures app.

Defines URL patterns for procedure charts and list views.
"""


from django.urls import path
from . import views

app_name = "procedures"

urlpatterns = [
    path(
        "charts/<int:mechanism_id>/",
        views.ProcedureChartsView.as_view(),
        name="procedure_charts",
    ),
    path("charts/", views.ProcedureChartsView.as_view(), name="procedure_charts"),
    path("charts/", views.ProcedureChartsView.as_view(), name="procedure_charts_query"),
    path("", views.ProcedureListView.as_view(), name="procedure_list"),
]
