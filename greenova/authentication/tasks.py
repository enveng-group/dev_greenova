"""Background and manual tasks for the authentication app.

All functions and classes are decorated with @beartype for runtime type checking.
"""
from beartype import beartype
import logging
from django.contrib.sessions.models import Session
from django.utils import timezone
from .types import UserInfoDict, SessionDataDict, Authenticator, SessionManager

logger = logging.getLogger(__name__)

@beartype
def cleanup_expired_sessions() -> None:
    """Remove expired authentication sessions from the session store."""
    now = timezone.now()
    expired_sessions = Session.objects.filter(expire_date__lt=now)
    count = expired_sessions.count()
    expired_sessions.delete()
    logger.info("Deleted %d expired sessions", count)
