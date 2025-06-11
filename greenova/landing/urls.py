"""URL configuration for the landing app."""

from django.urls import path

from .views import HomeView, newsletter_signup

app_name = "landing"

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("newsletter-signup/", newsletter_signup, name="newsletter_signup"),
]
