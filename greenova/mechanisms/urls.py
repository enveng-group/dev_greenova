"""URL configuration for the mechanisms app.

Defines URL patterns for mechanisms list, charts, and insights views.
"""

from django.urls import path

from . import views

app_name = "mechanisms"

urlpatterns = [
    path(
        "", views.MechanismListView.as_view(), name="list"
    ),  # Fixed class name from MechanismsListView to MechanismListView
    path("charts/", views.MechanismChartView.as_view(), name="mechanism_charts"),
    path(
        "insights/", views.ObligationInsightView.as_view(), name="obligation_insights"
    ),
]
