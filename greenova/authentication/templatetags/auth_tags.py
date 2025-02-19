from django import template
from django.contrib.auth import get_user_model
from django.template.defaultfilters import safe
from typing import Any, Dict, Optional
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

@register.inclusion_tag('authentication/components/user_menu.html', takes_context=True)
def user_menu(context: Dict[str, Any]) -> Dict[str, Any]:
    """Render user menu with authentication status."""
    try:
        request = context.get('request')
        return {
            'user': request.user if request else None,
            'is_authenticated': request.user.is_authenticated if request else False,
            'display_name': get_display_name(request.user) if request and request.user.is_authenticated else None
        }
    except Exception as e:
        logger.error(f"Error rendering user menu: {str(e)}")
        return {'error': True}

@register.simple_tag(takes_context=True)
def auth_status(context: Dict[str, Any]) -> Dict[str, Any]:
    """Get authentication status and user info."""
    try:
        request = context.get('request')
        user = request.user if request else None
        if user and user.is_authenticated:
            return {
                'is_authenticated': True,
                'username': user.username,
                'display_name': get_display_name(user),
                'is_staff': user.is_staff
            }
        return {
            'is_authenticated': False,
            'username': None,
            'display_name': None,
            'is_staff': False
        }
    except Exception as e:
        logger.error(f"Error getting auth status: {str(e)}")
        return {
            'is_authenticated': False,
            'error': True
        }

@register.inclusion_tag('authentication/components/forms/field.html')
def render_field(field: Any, help_text: str = '') -> Dict[str, Any]:
    """Render form field with consistent styling."""
    return {
        'field': field,
        'help_text': help_text or field.help_text,
        'field_id': field.id_for_label,
        'errors': field.errors
    }