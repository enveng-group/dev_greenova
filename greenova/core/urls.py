"""URL configuration for the Greenova core app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from django.urls import path

from .views import (
    EnvironmentalObligationListView,
    audit_log_api,
    audit_log_list_view,
    obligations_api,
    profile_detail_view,
    profile_edit_view,
    theme_config_api,
)

app_name = "core"

urlpatterns = [
    path(
        "obligations/",
        EnvironmentalObligationListView.as_view(),
        name="obligation_list",
    ),
    path(
        "api/obligations/",
        obligations_api,
        name="obligations_api",
    ),
    path("profile/", profile_detail_view, name="profile_detail"),
    path("profile/edit/", profile_edit_view, name="profile_edit"),
    path(
        "api/theme/",
        theme_config_api,
        name="theme_config_api",
    ),
    path(
        "audit-log/",
        audit_log_list_view,
        name="audit_log_list",
    ),
    path(
        "api/audit-log/",
        audit_log_api,
        name="audit_log_api",
    ),
]
