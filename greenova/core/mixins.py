"""Copyright (C) 2025 Adrian Gallo.

This file is part of Greenova.

Greenova is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Greenova is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Greenova. If not, see <https://www.gnu.org/licenses/>.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

"""Mixins for reusable view logic in the Greenova core app.

This module provides mixins for breadcrumbs, page titles, and active section
context in views.
"""


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin
from typing import Any, ClassVar, TypeVar

# Define a type variable for views with context data
ContextView = TypeVar("ContextView", bound=ContextMixin)


class BreadcrumbMixin(ContextMixin):
    """Add breadcrumb data to template context.

    Usage:
        class MyView(BreadcrumbMixin, TemplateView):
            breadcrumbs = [
                ('Home', 'home'),
                ('Dashboard', 'dashboard:home'),
                ('Current Page', None),  # None for current page with no link
            ]
    """

    breadcrumbs: ClassVar[list[tuple[str, str | None]]] = []

    def get_breadcrumbs(self) -> list[tuple[str, str | None]]:
        """Get breadcrumbs for this view."""
        return self.breadcrumbs

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        """Add breadcrumbs to the template context.

        Args:
            **kwargs: Arbitrary keyword arguments for context.

        Returns:
            Context dictionary with breadcrumbs included.

        """
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = self.get_breadcrumbs()
        return context


class PageTitleMixin(ContextMixin):
    """Add page title to template context.

    Usage:
        class MyView(PageTitleMixin, TemplateView):
            page_title = "My Page Title"
    """

    page_title: str | None = None

    def get_page_title(self) -> str | None:
        """Get page title for this view."""
        return self.page_title

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        """Add page title to the template context.

        Args:
            **kwargs: Arbitrary keyword arguments for context.

        Returns:
            Context dictionary with page title included.

        """
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.get_page_title()
        return context


class ActiveSectionMixin(ContextMixin):
    """Add active section to template context for navigation highlighting.

    Usage:
        class MyView(ActiveSectionMixin, TemplateView):
            active_section = "dashboard"
    """

    active_section: str | None = None

    def get_active_section(self) -> str | None:
        """Get active section for this view."""
        return self.active_section

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        """Add active section to the template context.

        Args:
            **kwargs: Arbitrary keyword arguments for context.

        Returns:
            Context dictionary with active section included.

        """
        context = super().get_context_data(**kwargs)
        context["active_section"] = self.get_active_section()
        return context


class ViewMixin(BreadcrumbMixin, PageTitleMixin, ActiveSectionMixin):
    """Combined mixin for standard view context data.

    Usage:
        class MyView(ViewMixin, TemplateView):
            page_title = "Dashboard"
            active_section = "dashboard"
            breadcrumbs = [('Home', 'home'), ('Dashboard', None)]
    """


class AuthViewMixin(LoginRequiredMixin, ViewMixin):
    """Combined mixin for authenticated views.

    Usage:
        class MyView(AuthViewMixin, TemplateView):
            page_title = "Dashboard"
            active_section = "dashboard"
            breadcrumbs = [('Home', 'home'), ('Dashboard', None)]
    """
