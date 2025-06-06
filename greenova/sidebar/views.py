"""Sidebar app views for Greenova.

Handles sidebar rendering and logic.
"""

from django.views.generic.base import TemplateView


class SidebarPartialView(TemplateView):
    """Renders the sidebar partial for dashboard UI."""

    template_name = "sidebar/sidebar_partial.jinja"


# Add views here
