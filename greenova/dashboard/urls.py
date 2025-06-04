from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardHomeView.as_view(), name="home"),
    # Drilldown views for Issue #165
    path(
        "mechanisms/",
        views.MechanismDrilldownView.as_view(),
        name="mechanism_drilldown"),
    path(
        "procedures/",
        views.ProcedureDrilldownView.as_view(),
        name="procedure_drilldown"),
    path(
        "obligations/",
        views.ObligationListDrilldownView.as_view(),
        name="obligation_list_drilldown"),
]
