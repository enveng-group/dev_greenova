import logging
from django.http import JsonResponse
from .exceptions import GreenovaException

logger = logging.getLogger(__name__)

def handle_dashboard_error(func):
    """Decorator to handle dashboard errors consistently."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except GreenovaException as e:
            logger.error(f"Dashboard error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
    return wrapper