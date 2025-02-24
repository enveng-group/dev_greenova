from typing import Dict, Any, Optional, Union
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import logging

logger = logging.getLogger(__name__)

class ResponseHandler:
    """Utility class for handling HTTP responses."""

    @staticmethod
    def set_htmx_trigger(response: HttpResponse, event_name: str) -> None:
        """
        Sets HX-Trigger header for HTMX events.

        Args:
            response: The HttpResponse object
            event_name: Name of the event to trigger
        """
        response['HX-Trigger'] = event_name

    @staticmethod
    def json_response(
        data: Dict[str, Any],
        status: int = 200,
        headers: Optional[Dict[str, str]] = None
    ) -> JsonResponse:
        """
        Creates a JSON response with proper headers.

        Args:
            data: Data to be serialized to JSON
            status: HTTP status code
            headers: Optional additional headers

        Returns:
            JsonResponse object
        """
        response = JsonResponse(
            data,
            status=status,
            encoder=DjangoJSONEncoder,
            safe=False
        )

        if headers:
            for key, value in headers.items():
                response[key] = value

        return response

    @staticmethod
    def html_response(
        content: str,
        status: int = 200,
        headers: Optional[Dict[str, str]] = None
    ) -> HttpResponse:
        """
        Creates an HTML response with proper headers.

        Args:
            content: HTML content string
            status: HTTP status code
            headers: Optional additional headers

        Returns:
            HttpResponse object
        """
        response = HttpResponse(
            content,
            status=status,
            content_type='text/html'
        )

        if headers:
            for key, value in headers.items():
                response[key] = value

        return response

    @staticmethod
    def error_response(
        message: str,
        status: int = 400,
        headers: Optional[Dict[str, str]] = None
    ) -> JsonResponse:
        """
        Creates an error response with proper headers.

        Args:
            message: Error message
            status: HTTP status code
            headers: Optional additional headers

        Returns:
            JsonResponse object
        """
        data = {
            'error': message,
            'status': status
        }

        response = JsonResponse(
            data,
            status=status
        )

        if headers:
            for key, value in headers.items():
                response[key] = value

        return response

    @staticmethod
    def htmx_response(
        content: Union[str, Dict[str, Any]],
        trigger_event: Optional[str] = None,
        status: int = 200,
        headers: Optional[Dict[str, str]] = None
    ) -> HttpResponse:
        """
        Creates a response specifically for HTMX requests.

        Args:
            content: Response content (HTML string or JSON data)
            trigger_event: Optional HTMX event to trigger
            status: HTTP status code
            headers: Optional additional headers

        Returns:
            HttpResponse object
        """
        if isinstance(content, dict):
            response = JsonResponse(content, status=status)
        else:
            response = HttpResponse(content, status=status)

        if trigger_event:
            response['HX-Trigger'] = trigger_event

        if headers:
            for key, value in headers.items():
                response[key] = value

        return response

# Initialize a global instance for easy import
response_handler = ResponseHandler()
