from django import template
from typing import Any, Dict
from django.contrib.auth.models import User
import logging

# Set up logger
logger = logging.getLogger(__name__)

# Register template tags
register = template.Library()


@register.filter
def get_display_name(user: User) -> str:
    """Get user's display name, preferring first name if available."""
    try:
        if user.first_name:
            return user.first_name
        if user.get_full_name():
            return user.get_full_name()
        return user.username
    except Exception as e:
        logger.error(f"Error getting display name: {str(e)}")
        return "User"


@register.simple_tag(takes_context=True)
def user_greeting(context: Dict[str, Any]) -> str:
    """Generate personalized greeting based on user authentication status."""
    try:
        request = context.get('request')
        if request and request.user.is_authenticated:
            # Add debug logging
            logger.debug(f"User authenticated. Username: {request.user.username}")
            logger.debug(f"First name: {request.user.first_name}")
            logger.debug(f"Full name: {request.user.get_full_name()}")

            # More specific greeting logic
            if request.user.first_name:
                return f"Hi {request.user.first_name}"
            elif request.user.get_full_name():
                return f"Hi {request.user.get_full_name()}"
            return f"Hi {request.user.username}"
        logger.debug("User not authenticated")
        return "Welcome Guest"
    except Exception as e:
        logger.error(f"Error generating greeting: {str(e)}")
        return "Welcome"
