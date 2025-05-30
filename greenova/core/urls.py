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

"""URL configuration for the Greenova core app.

This module defines URL patterns for core system endpoints and error pages.
"""

from . import views
from django.urls import path
from django.views.generic import TemplateView


app_name = "core"

urlpatterns = [
    path("health/", views.HealthCheckView.as_view(), name="health_check"),
    # Error pages for testing/development
    path(
        "error/400/",
        TemplateView.as_view(template_name="errors/400.html"),
        name="error_400",
    ),
    path(
        "error/403/",
        TemplateView.as_view(template_name="errors/403.html"),
        name="error_403",
    ),
    path(
        "error/404/",
        TemplateView.as_view(template_name="errors/404.html"),
        name="error_404",
    ),
    path(
        "error/500/",
        TemplateView.as_view(template_name="errors/500.html"),
        name="error_500",
    ),
]
