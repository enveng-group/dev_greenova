"""Navigation app views for Greenova.

Handles navigation, breadcrumbs, and project selector.
"""

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
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


# Add views here
