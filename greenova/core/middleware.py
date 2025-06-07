"""Audit middleware for Greenova core app.

Tracks user actions and system events for audit trail.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from collections.abc import Callable

from beartype import beartype
from django.http import HttpRequest, HttpResponse

from .audit_utils import log_audit_event
from .models import CustomUser


class AuditMiddleware:
    """Middleware to log user actions for auditing purposes."""

    @beartype
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    @beartype
    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        # Example: log all POST requests as audit events
        if request.method == "POST" and request.user.is_authenticated:
            log_audit_event(
                user=request.user if isinstance(request.user, CustomUser) else None,
                action="post_request",
                object_type="URL",
                object_id=request.path,
                message=f"POST to {request.path}",
                ip_address=request.META.get("REMOTE_ADDR"),
            )
        return response
