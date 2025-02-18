from typing import Any
from django.views.generic import View
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class ChatApiView(View):
    """Handle chat API requests."""

    def get(self, request: HttpRequest) -> JsonResponse:
        """Handle GET requests - return API info."""
        return JsonResponse({
            'status': 'active',
            'message': 'Chat API endpoint is ready',
            'version': '1.0'
        })

    def post(self, request: HttpRequest) -> JsonResponse:
        """Handle POST requests for chat messages."""
        try:
            # Parse and validate request data
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            
            if not message:
                return JsonResponse({
                    "error": "Message is required",
                    "status": "error"
                }, status=400)

            # Process message (placeholder for actual chat logic)
            context = {
                'page': request.GET.get('page', 'unknown'),
                'user': request.user.get_username() if request.user.is_authenticated else 'guest'
            }
            
            response = {
                "status": "success",
                "message": f"I received: {message}",
                "context": context
            }
            
            logger.info(f"Chat message processed: {message[:50]}...")
            return JsonResponse(response)
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON in chat request")
            return JsonResponse({
                "error": "Invalid JSON format",
                "status": "error"
            }, status=400)
            
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            return JsonResponse({
                "error": "Internal server error",
                "status": "error",
                "details": str(e) if settings.DEBUG else None
            }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def chat_api_legacy(request: HttpRequest) -> JsonResponse:
    """Legacy function-based view for chat API - redirects to class-based view."""
    view = ChatApiView.as_view()
    response = view(request)
    return JsonResponse(response.content, safe=False)