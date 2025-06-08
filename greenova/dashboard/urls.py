"""Copyright (C) 2024 Adrian Gallo <agallo@enveng-group.com.au>
This file is part of Greenova and is licensed under the AGPL-3.0.

Dashboard app URLs for Greenova.
"""

from django.urls import path

from .views import DashboardIndexView

urlpatterns = [
    path("", DashboardIndexView.as_view(), name="index"),
]
