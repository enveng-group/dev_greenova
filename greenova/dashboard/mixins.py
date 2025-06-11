# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
View mixins for the dashboard application.

This module provides mixins that can be used with Django views to add
dashboard-specific functionality and context data.
"""

import base64
import logging
from typing import Any

from core.mixins import BreadcrumbMixin, PageTitleMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.utils import timezone
from projects.models import Project

from .figures import (
    create_obligations_status_chart,
    create_project_compliance_chart,
    create_timeline_chart,
)

logger = logging.getLogger(__name__)


class ChartMixin:
    """Stub mixin for chart-related dashboard views."""


class ProjectAwareDashboardMixin:
    """Stub mixin for project-aware dashboard views."""


class DashboardContextMixin(LoginRequiredMixin, BreadcrumbMixin, PageTitleMixin):
    """
    Mixin for dashboard views that provides common context data.

    This mixin handles project selection persistence and provides chart data
    for the dashboard views.
    """

    page_title = "Dashboard"
    breadcrumbs = [("Dashboard", None)]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Add dashboard-specific context data."""
        context = super().get_context_data(**kwargs)

        # Get the current user

        # Get the currently selected project from session or query parameters
        current_project_id = self._get_current_project_id()

        # Add project selection to context
        context["projects"] = self._get_user_projects()
        context["current_project_id"] = current_project_id

        # Generate charts and statistics
        self._add_chart_data(context, current_project_id)
        self._add_statistics(context, current_project_id)

        return context

    def _get_current_project_id(self) -> int | None:
        """
        Get the currently selected project ID.

        The ID comes from:
        1. Request query parameter (highest priority)
        2. Session storage (if available)
        3. None (if no project is selected)
        """
        # First check if we have a project_id in the query string
        project_id = self.request.GET.get("project_id")

        # If not, check the session
        if not project_id and hasattr(self.request, "session"):
            project_id = self.request.session.get("dashboard_project_id")

        # Convert to integer if we have a project ID
        if project_id:
            try:
                return int(project_id)
            except (ValueError, TypeError):
                logger.warning("Invalid project ID: %s", project_id)

        return None

    def _get_user_projects(self):
        """Get projects associated with the current user."""
        return Project.objects.filter(
            # Filter conditions depending on user permissions
            # For now, just return all projects
        ).order_by("name")

    def _add_chart_data(self, context: dict[str, Any], project_id: int | None) -> None:
        """
        Add chart data to the context.

        Args:
            context: The context dictionary to update
            project_id: The current project ID (if any)
        """
        try:
            # Generate obligation status chart
            _, status_chart_data = create_obligations_status_chart(project_id)
            context["status_chart"] = base64.b64encode(status_chart_data).decode(
                "utf-8"
            )

            # Generate timeline chart
            _, timeline_chart_data = create_timeline_chart(project_id)
            context["timeline_chart"] = base64.b64encode(timeline_chart_data).decode(
                "utf-8"
            )

            # Generate project compliance chart if no specific project is selected
            if not project_id:
                projects = self._get_user_projects()
                _, compliance_chart_data = create_project_compliance_chart(projects)
                context["compliance_chart"] = base64.b64encode(
                    compliance_chart_data
                ).decode("utf-8")

        except Exception as e:
            logger.exception("Error generating chart data: %s", e)
            context["chart_error"] = str(e)

    def _add_statistics(self, context: dict[str, Any], project_id: int | None) -> None:
        """
        Add dashboard statistics to the context.

        Args:
            context: The context dictionary to update
            project_id: The current project ID (if any)
        """
        from obligations.models import Obligation

        filters = {}
        if project_id:
            filters["project_id"] = project_id

        # Get overall counts
        total_obligations = Obligation.objects.filter(**filters).count()

        # Count by status
        status_counts = dict(
            Obligation.objects.filter(**filters)
            .values("status")
            .annotate(count=Count("status"))
            .values_list("status", "count")
        )

        # Count overdue obligations
        now = timezone.now().date()
        overdue_count = Obligation.objects.filter(
            action_due_date__lt=now, status__in=["pending", "in_progress"], **filters
        ).count()

        # Calculate percentages
        if total_obligations > 0:
            completed_pct = round(
                (status_counts.get("completed", 0) / total_obligations) * 100
            )
            overdue_pct = round((overdue_count / total_obligations) * 100)
        else:
            completed_pct = 0
            overdue_pct = 0

        # Add to context
        context.update(
            {
                "total_obligations": total_obligations,
                "completed_count": status_counts.get("completed", 0),
                "in_progress_count": status_counts.get("in_progress", 0),
                "pending_count": status_counts.get("pending", 0),
                "overdue_count": overdue_count,
                "completed_pct": completed_pct,
                "overdue_pct": overdue_pct,
            }
        )
