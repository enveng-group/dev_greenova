"""URL configuration for the projects app.

Defines URL patterns for project list, selection, and API endpoints.
"""
from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="project_list"),
    path("select/", views.ProjectSelectionView.as_view(), name="select"),
    path(
        "api/projects/<str:project_id>/obligations/",
        views.project_obligations,
        name="project_obligations",
    ),
]
