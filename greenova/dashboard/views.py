"""Dashboard app views for Greenova.

Handles dashboard logic for authenticated users.
"""

from typing import Any

from core.context_processors import projects_context
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class DashboardIndexView(LoginRequiredMixin, TemplateView):
    """Main dashboard view for authenticated users."""

    template_name = "dashboard/dashboard_home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Add dashboard context here (projects, mechanisms, etc.)
        context.update(projects_context(self.request))
        return context
