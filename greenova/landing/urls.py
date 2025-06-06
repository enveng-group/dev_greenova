from django.urls import path

from .views import HomeView, TestPartialView

app_name = "landing"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("test-partial/", TestPartialView.as_view(), name="test-partial"),
]
