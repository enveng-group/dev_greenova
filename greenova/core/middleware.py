"""Audit middleware for Greenova core app.

Tracks user actions and system events for audit trail.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from beartype import beartype
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

from .audit_utils import log_audit_event

if TYPE_CHECKING:
    from .models import CustomUser


class AuditMiddleware(MiddlewareMixin):
    """Middleware to log user actions for audit trail."""

    @beartype
    def process_view(
        self,
        request: HttpRequest,
        view_func: Callable[..., HttpResponse],
        view_args: tuple[Any, ...],
        view_kwargs: dict[str, Any],
    ) -> None:
        if request.user.is_authenticated and hasattr(request.user, "pk"):
            user: CustomUser = request.user  # type: ignore
            action = f"{request.method.lower()}_{view_func.__name__}"
            log_audit_event(
                user=user,
                action=action,
                object_type=view_func.__module__,
                object_id="",
                message=f"User {user.username} performed {action}",
                ip_address=request.META.get("REMOTE_ADDR"),
            )
