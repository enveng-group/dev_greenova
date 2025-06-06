from django.urls import path


from . import views
from django.urls import path

app_name = "mechanisms"

urlpatterns = [
    path("charts/", views.MechanismChartView.as_view(), name="mechanism_charts"),
    path("", views.MechanismListView.as_view(), name="list"),
]
