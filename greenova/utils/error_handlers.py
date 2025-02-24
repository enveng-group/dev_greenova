import logging
from typing import Callable, TypeVar, cast, Any
from django.http import JsonResponse, HttpResponse
from django.http.request import HttpRequest
from .exceptions import GreenovaException

logger = logging.getLogger(__name__)

ResponseType = TypeVar('ResponseType', bound=HttpResponse)
ViewFuncType = Callable[[HttpRequest, tuple[Any, ...], dict[str, Any]], ResponseType]

def handle_dashboard_error(func: ViewFuncType) -> ViewFuncType:
    """Decorator to handle dashboard errors with HTMX support."""
    def wrapper(request: HttpRequest, *args: Any, **kwargs: Any) -> ResponseType:
        try:
            return func(request, args, kwargs)
        except GreenovaException as e:
            logger.error(f"Dashboard error: {str(e)}")
            if getattr(request, 'htmx', False):
                return cast(ResponseType, HttpResponse(
                    f'<div class="error" role="alert">{str(e)}</div>',
                    status=400
                ))
            return cast(ResponseType, JsonResponse({'error': str(e)}, status=400))
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            if getattr(request, 'htmx', False):
                return cast(ResponseType, HttpResponse(
                    '<div class="error" role="alert">An unexpected error occurred</div>',
                    status=500
                ))
            return cast(ResponseType, JsonResponse({'error': 'An unexpected error occurred'}, status=500))
    return cast(ViewFuncType, wrapper)
