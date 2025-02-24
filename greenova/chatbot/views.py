from typing import Any, TypedDict, Dict, Optional
from datetime import datetime
from django.views.generic import View
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .services import ChatService
from .forms import ChatMessageForm
import logging

logger = logging.getLogger(__name__)

class ChatResponse(TypedDict):
    status: str
    message: str
    context: Dict[str, str]
    error: Optional[str]

@method_decorator(csrf_exempt, name='dispatch')
class ChatApiView(View):
    """Handle chat API requests."""

    http_method_names = ['get', 'post']  # Explicitly define allowed methods

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """Handle GET requests - return API info."""
        response: ChatResponse = {
            'status': 'active',
            'message': 'Chat API endpoint is ready',
            'context': {},
            'error': None
        }
        return JsonResponse(response)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """Handle POST requests for chat messages."""
        try:
            form = ChatMessageForm(request.POST)

            if not form.is_valid():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid form data',
                    'context': {},
                    'error': form.errors
                }, status=400)

            message = form.cleaned_data['message']
            chat_service = ChatService()
            result = chat_service.process_message(message)

            return JsonResponse({
                'status': 'success',
                'message': result['message'],
                'context': result['context'],
                'error': None
            })

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'An unexpected error occurred',
                'context': {},
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ChatToggleView(View):
    """Handle chat widget toggle state."""

    http_method_names = ['get', 'post']  # Explicitly define allowed methods

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """Return chat dialog state."""
        return JsonResponse({
            "isOpen": False,
            "messages": [],
            "timestamp": datetime.now().isoformat()
        })

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """Handle dialog state toggle."""
        return JsonResponse({
            "isOpen": True,
            "messages": [],
            "timestamp": datetime.now().isoformat()
        })


@csrf_exempt
@require_http_methods(["POST"])
def chat_api_legacy(request: HttpRequest) -> JsonResponse:
    """Legacy function-based view for chat API - redirects to class-based view."""
    view = ChatApiView.as_view()
    response = view(request)
    return JsonResponse(response.content, safe=False)
