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
