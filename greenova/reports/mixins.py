"""mixins.py.

Reusable mixin classes for the reports app.

This module provides mixins that encapsulate shared logic for views, models, or forms.
Add new mixins here to promote code reuse and maintainability.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from .permissions import user_can_view_report


@beartype
class ReportPermissionRequiredMixin:
    """Mixin to enforce permission checks for report views."""

    error_message: str = "You do not have permission to view this report."

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        report = self.get_object()
        if not user_can_view_report(request.user, report):
            messages.error(request, self.error_message)
            return redirect("dashboard:home")
        return super().dispatch(request, *args, **kwargs)


@beartype
class ReportContextMixin:
    """Mixin to add common report context data to views."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = self.get_object() if hasattr(self, "get_object") else None
        if report:
            context["report_id"] = report.id
        return context
