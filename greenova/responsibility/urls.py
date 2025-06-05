from django.urls import path

from . import views
from .views import export_responsibility, export_all_responsibilities, import_responsibility

app_name = "responsibility"

urlpatterns = [
    path(
        "chart/",
        views.ResponsibilityChartView.as_view(),
        name="responsibility_chart"),
    path(
        "api/options/",
        views.get_responsibility_options,
        name="responsibility_options"),
    path("export/<int:responsibility_id>/", export_responsibility, name="export_responsibility"),
    path("export-all/", export_all_responsibilities, name="export_all_responsibilities"),
    path("import/", import_responsibility, name="import_responsibility"),
]
