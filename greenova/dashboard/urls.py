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

"""URL configuration for the dashboard app.

Defines URL patterns for dashboard views, including the home page,
upcoming obligations, and projects at risk.

Author:
    Adrian Gallo (agallo@enveng-group.com.au)
"""


from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path(
        "",
        views.DashboardHomeView.as_view(),
        name="home"),
    path(
        "upcoming-obligations/",
        views.UpcomingObligationsView.as_view(),
        name="upcoming_obligations",
    ),
    path(
        "projects-at-risk/",
        views.ProjectsAtRiskView.as_view(),
        name="projects_at_risk",
    ),
]
