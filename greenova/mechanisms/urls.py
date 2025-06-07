import logging

from django.urls import path

from . import views

logger = logging.getLogger(__name__)


app_name = "mechanisms"

urlpatterns = [
    path("charts/", views.MechanismChartView.as_view(), name="mechanism_charts"),
    path("", views.MechanismListView.as_view(), name="list"),
]
