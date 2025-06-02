"""Signal handlers for the core application."""

import logging
from typing import Any

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpRequest

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def log_user_login(
        sender: Any,
        request: HttpRequest,
        user: User,
        **kwargs: Any) -> None:
    """Log when a user logs in."""
    logger.info(f"User logged in: {user.username}")


@receiver(user_logged_in)
@receiver(user_logged_out)
def log_user_logout(
        sender: Any,
        request: HttpRequest,
        user: User | None,
        **kwargs: Any) -> None:
    """Log when a user logs out."""
    if user:
        logger.info(f"User logged out: {user.username}")
    else:
        logger.info("Anonymous user logged out")


@receiver(post_save, sender=User)
def handle_user_update(
        sender: type[User],
        instance: User,
        created: bool,
        **kwargs: Any) -> None:
    """Handle user creation and updates."""
    if created:
        logger.info(f"New user created: {instance.username}")
    else:
        logger.debug(f"User updated: {instance.username}")
    """Register all signal handlers."""


def register_signals() -> None:
    """Register all signal handlers."""
    # Will contain actual signal handlers as needed
