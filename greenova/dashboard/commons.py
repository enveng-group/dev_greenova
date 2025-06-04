"""commons.py.

Shared logic, helpers, and base classes for the dashboard app.

This module centralizes reusable code to improve maintainability and reduce duplication.
"""

import logging
from typing import Any, TypedDict

logger = logging.getLogger(__name__)

# Centralized color schemes for dashboard charts (used in figures.py, plotlyapp.py)
STATUS_COLORS = {
    "Not Started": "#f9c74f",  # Yellow
    "In Progress": "#90be6d",  # Green
    "Completed": "#43aa8b",  # Teal
    "Overdue": "#f94144",  # Red
}

PHASE_COLORS = {
    "Planning": "#3498db",  # Blue
    "Implementation": "#e67e22",  # Orange
    "Monitoring": "#9b59b6",  # Purple
    "Reporting": "#1abc9c",  # Turquoise
}


class DashboardContext(TypedDict):
    """Type definition for dashboard context data."""

    projects: Any
    selected_project_id: str | None
    system_status: str
    app_version: str
    last_updated: Any
    user: Any
    debug: bool
    error: str | None
    user_roles: dict[str, str]


# Add additional shared helpers or base classes here as needed.
