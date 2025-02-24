from typing import Dict, Any
from django.http import HttpRequest
from utils.constants import (
    SYSTEM_STATUS_OPERATIONAL,
    APP_VERSION,
    LAST_UPDATED
)


def greenova_context(request: HttpRequest) -> Dict[str, Any]:
    """Add common Greenova context data to all templates."""
    return {
        'system_status': SYSTEM_STATUS_OPERATIONAL,
        'app_version': APP_VERSION,
        'last_updated': LAST_UPDATED,  # Add this line
        'is_authenticated': request.user.is_authenticated,
        'show_landing_content': not request.user.is_authenticated and request.path.startswith('/landing/'),
        'show_dashboard_link': request.user.is_authenticated,

    }
