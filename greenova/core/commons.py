<<<<<<< HEAD
import logging
from typing import Any, Dict

from django.conf import settings
from django.http import HttpRequest

logger = logging.getLogger(__name__)


=======
from typing import Dict, List, Optional, Any, Union
from django.http import HttpRequest
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
def get_active_namespace(request: HttpRequest) -> str:
    """Get the active namespace from the request."""
    try:
        if hasattr(request, 'resolver_match') and request.resolver_match:
            return request.resolver_match.namespace or ''
<<<<<<< HEAD
    except AttributeError as e:
        logger.error("Error getting namespace: %s", str(e))
    return ''


=======
    except Exception as e:
        logger.error(f"Error getting namespace: {e}")
    return ''

>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
def get_user_display_name(user) -> str:
    """Get the best display name for a user."""
    if hasattr(user, 'get_full_name') and callable(user.get_full_name):
        full_name = user.get_full_name()
        if full_name:
            return full_name

    return user.username if hasattr(user, 'username') else str(user)

def get_app_settings() -> Dict[str, Any]:
    """Get application settings for templates."""
    return {
        'APP_VERSION': getattr(settings, 'APP_VERSION', 'dev'),
        'DEBUG': getattr(settings, 'DEBUG', False),
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'Greenova'),
        'SITE_DESCRIPTION': getattr(settings, 'SITE_DESCRIPTION',
<<<<<<< HEAD
                                    'Environmental Compliance Management System'),
=======
                              'Environmental Compliance Management System'),
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
    }
