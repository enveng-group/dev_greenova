"""Background and manual tasks for the users app.

All functions and classes are decorated with @beartype for runtime type checking.
"""
from beartype import beartype
import logging
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .types import UserProfileDict, UserPermissionsDict, SessionDataDict, UserProfileManager, PermissionManager, UserSessionManager

logger = logging.getLogger(__name__)

@beartype
def send_welcome_emails() -> None:
    """Send welcome emails to new users who have not received one, mark as sent, and log the action."""
    # Assume Profile model has a boolean field 'welcome_email_sent'
    from .models import Profile
    new_profiles = Profile.objects.filter(welcome_email_sent=False)
    count = 0
    for profile in new_profiles:
        user = profile.user
        if not user.email:
            continue
        subject = "Welcome to Greenova!"
        message = (
            f"Hello {user.username},\n\n"
            "Welcome to Greenova, the environmental management platform. "
            "We're glad to have you on board!"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
        profile.welcome_email_sent = True
        profile.save(update_fields=["welcome_email_sent"])
        logger.info("Sent welcome email to user %s", user.username)
        count += 1
    logger.info("Sent %d welcome emails to new users.", count)
