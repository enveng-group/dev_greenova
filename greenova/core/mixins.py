"""Reusable mixin classes for Greenova apps.

These mixins encapsulate shared logic for views, models, or forms and are available for use across all apps.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any

from beartype import beartype
from core.permissions import user_can_view_obligation, user_can_view_project
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from responsibility.models import ResponsibilityAssignment


@beartype
class ProjectPermissionRequiredMixin:
    """Mixin to enforce role-based access control for project views."""

    required_roles: list[str] = ["owner", "manager"]
    error_message: str = "You do not have permission to perform this action."

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        project = self.get_object()
        if not user_can_view_project(request.user, project):
            messages.error(request, self.error_message)
            return redirect("dashboard:home")
        return super().dispatch(request, *args, **kwargs)


@beartype
class ProjectContextMixin:
    """Mixin to add common project context data to views."""

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        project = self.get_object() if hasattr(self, "get_object") else None
        if project:
            pass  # Add project-specific context here if needed
        return context


@beartype
def user_has_obligation_role(user: Any, obligation: Any, roles: list[str]) -> bool:
    """Check if the user has any of the specified roles for the obligation."""
    return ResponsibilityAssignment.objects.filter(
        obligation=obligation,
        user=user,
        role__in=roles,
    ).exists()


@beartype
class ObligationPermissionRequiredMixin:
    """Mixin to enforce role-based access control for obligation views."""

    required_roles: list[str] = ["Owner", "Editor"]
    error_message: str = "You do not have permission to perform this action."

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        obligation = self.get_object()
        if not user_can_view_obligation(request.user, obligation):
            messages.error(request, self.error_message)
            return redirect("dashboard:home")
        return super().dispatch(request, *args, **kwargs)


@beartype
class ObligationContextMixin:
    """Mixin to add common obligation context data to views."""

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        obligation = self.get_object() if hasattr(self, "get_object") else None
        if obligation:
            context["project_id"] = obligation.project_id
            context["user_can_edit"] = user_has_obligation_role(
                self.request.user,
                obligation,
                ["Editor", "Owner", "Manager"],
            )
        return context
