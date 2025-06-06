"""Sidebar app URLs for Greenova."""

from django.urls import path

from .views import SidebarPartialView

urlpatterns = [
    path("partial/", SidebarPartialView.as_view(), name="sidebar_partial"),
]
