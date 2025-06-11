from django.urls import path

from . import views

app_name = "mechanisms"

urlpatterns = [
    path(
        "", views.MechanismListView.as_view(), name="list"
    ),  # Fixed class name from MechanismsListView to MechanismListView
    path("charts/", views.MechanismChartView.as_view(), name="mechanism_charts"),
    path("charts/data/", views.mechanism_chart_data_json, name="mechanism_charts_json"),
]
