import logging
from typing import Any, Callable, TypeVar
from django.http import JsonResponse, HttpResponse
from django.http.request import HttpRequest
from .exceptions import GreenovaException
from functools import wraps
from django.views import View

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=Callable[..., HttpResponse])

def handle_view_error(func: T) -> T:
    """Decorator for handling errors in view functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"View error: {str(e)}", exc_info=True)
            if isinstance(args[0], View):
                from django.shortcuts import render
                template_name = getattr(args[0], 'template_name', 'error.html')  # use default if not found
                return render(args[0].request, template_name, {'error': str(e)})
                return HttpResponse(f'Error: {str(e)}', status=500)
            return JsonResponse({'error': str(e)}, status=500)
    return wrapper  # type: ignore

def handle_error(view_class: Any) -> Any:
    """Class decorator to handle errors in class-based views."""
    if hasattr(view_class, 'dispatch'):
        original_dispatch = view_class.dispatch

        def new_dispatch(self, request, *args, **kwargs):
            try:
                return original_dispatch(self, request, *args, **kwargs)
            except Exception as e:
                logger.error(f"View error: {str(e)}", exc_info=True)
                return self.render_to_response({'error': str(e)})

        view_class.dispatch = new_dispatch
    return view_class

def api_error_handler(func: T) -> T:
    """Decorator for handling errors in API views."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"API error: {str(e)}", exc_info=True)
            return JsonResponse({
                'error': str(e),
                'status': 'error'
            }, status=500)
    return wrapper  # type: ignore
