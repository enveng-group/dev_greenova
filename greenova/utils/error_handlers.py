import logging
from django.http import JsonResponse, HttpResponse
from .exceptions import GreenovaException

logger = logging.getLogger(__name__)

def handle_dashboard_error(func):
    """Decorator to handle dashboard errors with HTMX support."""
    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except GreenovaException as e:
            logger.error(f"Dashboard error: {str(e)}")
            if request.htmx:
                return HttpResponse(
                    f'<div class="error" role="alert">{str(e)}</div>',
                    status=400
                )
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            if request.htmx:
                return HttpResponse(
                    '<div class="error" role="alert">An unexpected error occurred</div>',
                    status=500
                )
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
    return wrapper