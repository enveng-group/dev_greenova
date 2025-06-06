"""Reusable mixin classes for Greenova apps.

These mixins encapsulate shared logic for views, models, or forms and are available for use across all apps.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from core.permissions import user_can_view_project
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


@beartype
class ProjectPermissionRequiredMixin:
    """Mixin to enforce role-based access control for project views."""

    required_roles: list[str] = ["owner", "manager"]
    error_message: str = "You do not have permission to perform this action."

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        project = self.get_object()
        # Use centralized permission function
        if not user_can_view_project(request.user, project):
            messages.error(request, self.error_message)
            return redirect("dashboard:home")
        return super().dispatch(request, *args, **kwargs)


@beartype
class ProjectContextMixin:
    """Mixin to add common project context data to views."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object() if hasattr(self, "get_object") else None
        if project:
            pass  # Add project-specific context here if needed
        return context
