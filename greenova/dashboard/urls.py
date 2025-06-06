"""Dashboard app URLs for Greenova."""

from django.urls import path

from .views import DashboardIndexView

urlpatterns = [
    path("", DashboardIndexView.as_view(), name="index"),
]
