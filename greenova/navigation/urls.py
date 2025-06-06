"""Navigation app URLs for Greenova."""

from django.urls import path

from .views import HeaderPartialView

urlpatterns = [
    path("header/", HeaderPartialView.as_view(), name="header_partial"),
    # Add project selector POST endpoint later
]
