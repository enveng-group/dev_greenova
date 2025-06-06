from django.urls import path
from .views import SettingsHomeView

app_name = "settings"

urlpatterns = [
    path("", SettingsHomeView.as_view(), name="home"),
]
