from django.urls import path

from . import views
from .views import ProjectListView

app_name = "projects"

urlpatterns = [
    path("select/", views.ProjectSelectionView.as_view(), name="select"),
    path(
        "api/projects/<str:project_id>/obligations/",
        views.project_obligations,
        name="project_obligations",
    ),
    path(
        "",
        ProjectListView.as_view(),
        name="project_list",
    ),
    # ProjectMembership protobuf API endpoints
    path(
        "api/project-memberships/<int:membership_id>/export/",
        views.export_project_membership,
        name="export_project_membership",
    ),
    path(
        "api/project-memberships/export-all/",
        views.export_all_project_memberships,
        name="export_all_project_memberships",
    ),
    path(
        "api/project-memberships/import/",
        views.import_project_membership,
        name="import_project_membership",
    ),
    # Project protobuf API endpoints
    path(
        "api/projects/<int:project_id>/export/",
        views.export_project,
        name="export_project",
    ),
    path(
        "api/projects/export-all/",
        views.export_all_projects,
        name="export_all_projects",
    ),
    path(
        "api/projects/import/",
        views.import_project,
        name="import_project",
    ),
]
