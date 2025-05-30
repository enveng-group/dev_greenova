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

"""URL configuration for the users app in Greenova.

Defines URL patterns for user profile management, listing, and admin management.
"""


from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # User profile URLs
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("profile/change-password/", views.change_password, name="change_password"),
    path(
        "profile/upload-image/", views.upload_profile_image, name="upload_profile_image",
    ),
    # User list URL
    path("list/", views.UserListView.as_view(), name="user_list"),
    # Admin user management URLs
    path("admin/users/", views.admin_user_list, name="admin_user_list"),
    path("admin/users/create/", views.admin_user_create, name="admin_user_create"),
    path(
        "admin/users/<int:user_id>/edit/", views.admin_user_edit, name="admin_user_edit",
    ),
    path(
        "admin/users/<int:user_id>/delete/",
        views.admin_user_delete,
        name="admin_user_delete",
    ),
]
