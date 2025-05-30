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

"""URL configuration for the responsibility app.

Defines URL patterns for responsibility home, assignments, and roles views.
"""


from django.urls import path
from . import views

app_name = "responsibility"

urlpatterns = [
    # Basic URLs - to be expanded later with actual views
    path("", views.responsibility_home, name="home"),
    path("assignments/", views.assignment_list, name="assignment_list"),
    path("roles/", views.role_list, name="role_list"),
]
