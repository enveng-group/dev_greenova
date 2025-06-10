"""Copyright (C) 2024 Adrian Gallo <agallo@enveng-group.com.au>
This file is part of Greenova and is licensed under the AGPL-3.0.

Dashboard app URLs for Greenova.
"""

from dashboard.api.protobuf_api import DashboardProtobufAPIView
from django.urls import path

from .views import (
    DashboardIndexView,
    DashboardProjectSummaryWidgetView,
    DashboardUnauthenticatedView,
)

urlpatterns = [
    path("", DashboardIndexView.as_view(), name="index"),
    path(
        "unauthenticated/",
        DashboardUnauthenticatedView.as_view(),
        name="dashboard_unauthenticated",
    ),
    path(
        "widget/project-summary/",
        DashboardProjectSummaryWidgetView.as_view(),
        name="dashboard_project_summary_widget",
    ),
    path(
        "api/protobuf/dashboard/",
        DashboardProtobufAPIView.as_view(),
        name="dashboard_protobuf_api",
    ),
]
