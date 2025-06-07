from django.urls import path

from . import views
from .views import (
    ProcedureListView,
    export_all_procedures,
    export_procedure,
    import_procedure,
)

app_name = "procedures"

urlpatterns = [
    path(
        "",
        ProcedureListView.as_view(),
        name="procedure_list",
    ),
    path(
        "charts/<int:mechanism_id>/",
        views.ProcedureChartsView.as_view(),
        name="procedure_charts",
    ),
    path("charts/", views.ProcedureChartsView.as_view(), name="procedure_charts_query"),
    path("export/<int:procedure_id>/", export_procedure, name="export_procedure"),
    path("export-all/", export_all_procedures, name="export_all_procedures"),
    path("import/", import_procedure, name="import_procedure"),
]
