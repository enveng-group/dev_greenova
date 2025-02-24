import logging
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def get_status_badge(status: str) -> str:
    """Generate HTML for status badge."""
    status_classes = {
        'not started': 'secondary',
        'in progress': 'primary',
        'completed': 'success',
        'overdue': 'error'
    }
    css_class = status_classes.get(status.lower(), 'secondary')
    logger.debug(f"Generated status badge for {status}")
    return mark_safe(f'<mark class="{css_class}">{status.title()}</mark>')


def get_user_display_name(user: User) -> str:
    """Get best display name for user."""
    return user.get_full_name() or user.username
