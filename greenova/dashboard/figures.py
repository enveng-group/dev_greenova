# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Chart generation utilities for the dashboard application.

This module provides functions for generating matplotlib charts
used in the dashboard views and components.
"""

import io
import logging

import matplotlib
import matplotlib.pyplot as plt
from django.db.models import Count
from obligations.models import Obligation

# Configure matplotlib for non-interactive backend to avoid GUI requirements
matplotlib.use("Agg")

# Set up logger
logger = logging.getLogger(__name__)


def create_obligations_status_chart(
    project_id: int | None = None,
) -> tuple[plt.Figure, bytes]:
    """Create a pie chart of obligation statuses."""
    filters = {}
    if project_id:
        filters["project_id"] = project_id

    # Use 'pk' for primary key, and only use fields that exist
    status_counts = (
        Obligation.objects.filter(**filters)
        .values("status")
        .annotate(count=Count("pk"))
        .order_by("status")
    )

    labels = [item["status"] for item in status_counts]
    sizes = [item["count"] for item in status_counts]

    fig, ax = plt.subplots()
    if sizes:
        ax.pie(sizes, labels=labels, autopct="%1.1f%%")
    else:
        ax.text(0.5, 0.5, "No data", ha="center", va="center")
    ax.set_title("Obligation Status Distribution")

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return fig, buf.getvalue()


def create_obligations_status_chart_svg(project_id=None):
    """Create an SVG chart of obligation statuses."""
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, "Obligations Status Chart", ha="center", va="center")
    buf = io.BytesIO()
    fig.savefig(buf, format="svg")
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue().decode("utf-8")


def create_timeline_chart(project_id: int | None = None) -> tuple[plt.Figure, bytes]:
    """Stub: Returns a blank chart for timeline."""
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, "Timeline Chart", ha="center", va="center")
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return fig, buf.getvalue()


def create_project_compliance_chart(projects) -> tuple[plt.Figure, bytes]:
    """Stub: Returns a blank chart for project compliance."""
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, "Project Compliance Chart", ha="center", va="center")
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return fig, buf.getvalue()
