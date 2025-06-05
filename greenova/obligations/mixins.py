"""mixins.py.

Reusable mixin classes for the obligations app.

This module provides mixins that encapsulate shared logic for views, models, or forms.
Add new mixins here to promote code reuse and maintainability.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from responsibility.models import ResponsibilityAssignment
from .models import Obligation
from .permissions import user_can_view_obligation

@beartype
def user_has_obligation_role(user, obligation, roles: list[str]) -> bool:
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

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        obligation = self.get_object()
        if not user_can_view_obligation(request.user, obligation):
            messages.error(request, self.error_message)
            return redirect("dashboard:home")
        return super().dispatch(request, *args, **kwargs)

@beartype
class ObligationContextMixin:
    """Mixin to add common obligation context data to views."""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obligation = self.get_object() if hasattr(self, "get_object") else None
        if obligation:
            context["project_id"] = obligation.project_id
            context["user_can_edit"] = user_has_obligation_role(
                self.request.user, obligation, ["Editor", "Owner", "Manager"]
            )
        return context
