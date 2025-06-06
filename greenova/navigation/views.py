"""Navigation app views for Greenova.

Handles navigation, breadcrumbs, and project selector.
"""

from typing import Any

from beartype import beartype
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView


class HeaderPartialView(LoginRequiredMixin, TemplateView):
    """Renders the header partial for dashboard UI."""

    template_name = "navigation/header_partial.jinja"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Example context; replace with real project/breadcrumb logic
        context["breadcrumbs"] = [
            {"label": "Dashboard", "url": "#"},
        ]
        context["projects"] = []  # Populate with user's projects
        context["current_project_id"] = None
        return context


class SelectProjectView(LoginRequiredMixin, View):
    """Handles project selection POST requests from the header partial."""

    @beartype
    def post(
        self,
        request: HttpRequest,
        *args: object,
        **kwargs: object,
    ) -> HttpResponse:
        project_id = request.POST.get("project_id")
        if project_id:
            request.session["current_project_id"] = project_id
            messages.success(request, "Project switched successfully.")
        else:
            messages.error(request, "No project selected.")
        # If HTMX request, return dashboard main content partial
        if request.headers.get("HX-Request") == "true":
            from dashboard.views import DashboardIndexView

            view = DashboardIndexView()
            view.setup(request)
            context = view.get_context_data()
            return TemplateResponse(request, "dashboard/_dashboard_main.html", context)
        # Otherwise, redirect to dashboard
        return HttpResponseRedirect(reverse("dashboard:index"))
