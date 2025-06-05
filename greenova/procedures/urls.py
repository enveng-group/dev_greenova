from django.urls import path, include

from . import views
from . import plotlyapp
from .views import export_procedure, export_all_procedures, import_procedure

app_name = "procedures"

urlpatterns = [
    path(
        "charts/<int:mechanism_id>/",
        views.ProcedureChartsView.as_view(),
        name="procedure_charts"),
    path(
        "charts/",
        views.ProcedureChartsView.as_view(),
        name="procedure_charts_query"),
    path("export/<int:procedure_id>/", export_procedure, name="export_procedure"),
    path("export-all/", export_all_procedures, name="export_all_procedures"),
    path("import/", import_procedure, name="import_procedure"),
]
