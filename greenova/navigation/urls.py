"""Navigation app URLs for Greenova."""

from django.urls import path

from .views import HeaderPartialView, SelectProjectView

urlpatterns = [
    path("header/", HeaderPartialView.as_view(), name="header_partial"),
    path("select_project/", SelectProjectView.as_view(), name="select_project"),
]
