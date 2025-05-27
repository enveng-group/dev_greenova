"""
Chatbot app configuration module.

Defines the Django AppConfig for the chatbot application, which manages
chatbot-related features and initialization.
"""
from django.apps import AppConfig


class ChatbotConfig(AppConfig):
    """Configuration for the chatbot app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "chatbot"
