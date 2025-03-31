<<<<<<< HEAD
"""Signal handlers for the core application."""

import logging
from typing import Any, Optional, Type

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpRequest

logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def log_user_login(sender: Any, request: HttpRequest, user: User, **kwargs: Any) -> None:
    """Log when a user logs in."""
    logger.info(f'User logged in: {user.username}')
@receiver(user_logged_in)
@receiver(user_logged_out)
def log_user_logout(sender: Any, request: HttpRequest, user: Optional[User], **kwargs: Any) -> None:
    """Log when a user logs out."""
    if user:
        logger.info(f'User logged out: {user.username}')
    else:
        logger.info('Anonymous user logged out')
@receiver(post_save, sender=User)
def handle_user_update(sender: Type[User], instance: User, created: bool, **kwargs: Any) -> None:
    """Handle user creation and updates."""
    if created:
        logger.info(f'New user created: {instance.username}')
    else:
        logger.debug(f'User updated: {instance.username}')
    """Register all signal handlers."""
def register_signals() -> None:
    """Register all signal handlers."""
    pass  # Will contain actual signal handlers as needed
=======
from django.dispatch import Signal, receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

# Custom signals
theme_preference_changed = Signal()  # Sent when user changes theme
navigation_accessed = Signal()  # Sent when user navigates to a new section

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Log when a user logs in."""
    logger.info(f"User logged in: {user.username}")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Log when a user logs out."""
    if user:
        logger.info(f"User logged out: {user.username}")
    else:
        logger.info("Anonymous user logged out")

@receiver(post_save, sender=User)
def handle_user_update(sender, instance, created, **kwargs):
    """Handle user creation and updates."""
    if created:
        logger.info(f"New user created: {instance.username}")
    else:
        logger.debug(f"User updated: {instance.username}")
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
