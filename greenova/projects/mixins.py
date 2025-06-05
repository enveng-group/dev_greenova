"""mixins.py.

Reusable mixin classes for the projects app.

This module provides mixins that encapsulate shared logic for views, models, or forms.
Add new mixins here to promote code reuse and maintainability.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from .models import Project
from .permissions import user_can_view_project

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
            context["project_id"] = project.id
            context["user_role"] = project.get_user_role(self.request.user)
        return context
