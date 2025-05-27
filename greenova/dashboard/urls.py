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
    path("", views.DashboardHomeView.as_view(), name="home"),
    path(
        "upcoming-obligations/",
        views.UpcomingObligationsView.as_view(),
        name="upcoming_obligations",
    ),
    path(
        "projects-at-risk/", views.ProjectsAtRiskView.as_view(), name="projects_at_risk"
    ),
]
