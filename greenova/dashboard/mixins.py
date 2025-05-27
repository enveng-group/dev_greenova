# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
View mixins for the dashboard application.

This module provides mixins that can be used with Django views to add
dashboard-specific functionality and context data.
"""

import logging
from typing import Any, ClassVar, cast  # Add cast

from beartype import beartype
from core.mixins import BreadcrumbMixin, PageTitleMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models  # Add this import for models.Q
from django.db.models import Count, QuerySet
from django.utils import timezone
from obligations.models import Obligation  # Moved to top-level import
from projects.models import Project

logger = logging.getLogger(__name__)


@beartype
class ChartMixin:
    """Stub mixin for chart-related dashboard views."""


@beartype
class ProjectAwareDashboardMixin:
    """Stub mixin for project-aware dashboard views."""


@beartype
class DashboardContextMixin(LoginRequiredMixin, BreadcrumbMixin, PageTitleMixin):
    """
    Mixin for dashboard views that provides common context data.

    This mixin handles project selection persistence and provides chart data
    for the dashboard views.
    """

    page_title = "Dashboard"
    breadcrumbs: ClassVar[list[tuple[str, None]]] = [("Dashboard", None)]

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Add dashboard-specific context data.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            A dictionary containing context data for the view.
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)

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

    @beartype
    def _get_current_project_id(self) -> int | None:
        """
        Get the currently selected project ID.

        The ID comes from:
        1. Request query parameter (highest priority)
        2. Session storage (if available)
        3. None (if no project is selected)

        Returns:
            The current project ID as an integer, or None if not found.
        """
        # First check if we have a project_id in the query string
        project_id_str = self.request.GET.get("project_id")

        # If not, check the session
        if not project_id_str and hasattr(self.request, "session"):
            project_id_str = self.request.session.get("dashboard_project_id")

        # Convert to integer if we have a project ID
        if project_id_str:
            try:
                return int(project_id_str)
            except (ValueError, TypeError):
                logger.warning("Invalid project ID: %s", project_id_str)

        return None

    @beartype
    def _get_user_projects(self) -> QuerySet[Project]:
        """
        Get projects associated with the current user.

        Returns:
            A QuerySet of Project objects.
        """
        user = self.request.user
        # Filter projects where the user is a member or owner.
        # Adjust the filter as per your Project model's fields.
        qs = (
            Project.objects.filter(models.Q(owner=user) | models.Q(members=user))
            .distinct()
            .order_by("name")
        )
        return cast(QuerySet[Project], qs)

    @beartype
    def _add_statistics(self, context: dict[str, Any], project_id: int | None) -> None:
        """
        Add dashboard statistics to the context.

        Args:
            context: The context dictionary to update.
            project_id: The current project ID (if any).
        """
        filters: dict[str, Any] = {}
        if project_id:
            filters["project_id"] = project_id

        # Get overall counts
        total_obligations = Obligation.objects.filter(**filters).count()

        # Count by status
        status_counts_qs = (
            Obligation.objects.filter(**filters)
            .values("status")
            .annotate(count=Count("status"))
            .values_list("status", "count")
        )
        status_counts: dict[str, int] = dict(status_counts_qs)

        # Count overdue obligations
        now = timezone.now().date()
        overdue_count = Obligation.objects.filter(
            action_due_date__lt=now, status__in=["pending", "in_progress"], **filters
        ).count()

        # Calculate percentages
        completed_pct = 0
        overdue_pct = 0
        if total_obligations > 0:
            completed_pct = round(
                (status_counts.get("completed", 0) / total_obligations) * 100
            )
            overdue_pct = round((overdue_count / total_obligations) * 100)

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
