"""Django application configuration for the feedback app."""

from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    """Application configuration for the Feedback app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "feedback"
