from typing import Any, TypedDict, Dict, Optional
from datetime import datetime
from django.views.generic import View
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .services import ChatService
from .forms import ChatMessageForm
import json
import logging
from django_htmx.http import trigger_client_event

logger = logging.getLogger(__name__)

class ChatResponse(TypedDict):
    status: str
    message: str
    context: Dict[str, str]
    error: Optional[str]

@method_decorator(csrf_exempt, name='dispatch')
class ChatApiView(View):
    """Handle chat API requests."""
    
    def get(self, request: HttpRequest) -> JsonResponse:
        """Handle GET requests - return API info."""
        response: ChatResponse = {
            'status': 'active',
            'message': 'Chat API endpoint is ready',
            'context': {},
            'error': None
        }
        return JsonResponse(response)

    def post(self, request: HttpRequest) -> JsonResponse:
        """Handle POST requests for chat messages."""
        try:
            form = ChatMessageForm(request.POST)
            
            if not form.is_valid():
                if request.htmx:  # Check if HTMX request
                    return HttpResponse(
                        f'<div class="error">{form.errors["message"][0]}</div>',
                        status=400
                    )
                return JsonResponse({
                    'status': 'error',
                    'message': '',
                    'context': {},
                    'error': form.errors['message'][0]
                }, status=400)

            message = form.cleaned_data['message']
            chat_service = ChatService()
            context = {
                'page': request.GET.get('page', 'unknown'),
                'user': request.user.get_username() if request.user.is_authenticated else 'guest'
            }
            
            response = chat_service.process_message(message, context)
            
            if request.htmx:
                # Return partial HTML for HTMX requests
                html = f"""
                <div class="message {response['status']}">
                    <p>{response['message']}</p>
                </div>
                """
                resp = HttpResponse(html)
                trigger_client_event(resp, 'chatMessageSent')
                return resp
                
            return JsonResponse(response)

        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            error_msg = str(e) if settings.DEBUG else 'Internal server error'
            if request.htmx:
                return HttpResponse(
                    f'<div class="error">{error_msg}</div>',
                    status=500
                )
            return JsonResponse({
                'status': 'error',
                'message': '',
                'context': {},
                'error': error_msg
            }, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class ChatToggleView(View):
    """Handle chat widget toggle state."""
    
    def get(self, request: HttpRequest) -> JsonResponse:
        """Return chat dialog state."""
        return JsonResponse({
            "isOpen": False,
            "messages": [],
            "timestamp": datetime.now().isoformat()
        })

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handle dialog state toggle."""
        if request.htmx:
            response = HttpResponse("<div>Chat opened</div>")
            trigger_client_event(response, 'chatOpened')
            return response
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