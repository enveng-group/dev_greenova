import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

logger = logging.getLogger(__name__)
User = get_user_model()

# Custom signals
theme_preference_changed = Signal()  # Sent when user changes theme
navigation_accessed = Signal()  # Sent when user navigates to a new section

@receiver(user_logged_in)
def log_user_login(_sender, _request, user, **_kwargs):
    """Log when a user logs in."""
    logger.info('User logged in: %s', user.username)

@receiver(user_logged_out)
def log_user_logout(_sender, _request, user, **_kwargs):
    """Log when a user logs out."""
    if user:
        logger.info('User logged out: %s', user.username)
    else:
        logger.info('Anonymous user logged out')

@receiver(post_save, sender=User)
def handle_user_update(_sender, instance, created, **_kwargs):
    """Handle user creation and updates."""
    if created:
        logger.info('New user created: %s', instance.username)
    else:
        logger.debug('User updated: %s', instance.username)
