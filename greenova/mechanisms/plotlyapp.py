"""Plotly middleware for mechanisms app.

This module acts as middleware between django_matplotlib (server-side SVG) and
plotly.js (client-side interactive charts), using the plotly Python package
for data serialization and chart generation.
"""

import logging
from typing import Any

import plotly.utils
from beartype import beartype

from .models import EnvironmentalMechanism

logger = logging.getLogger(__name__)

# Color scheme for consistency with matplotlib figures
STATUS_COLORS = {
    "Not Started": "#f9c74f",  # Yellow
    "In Progress": "#90be6d",  # Green
    "Completed": "#43aa8b",  # Teal
    "Overdue": "#f94144",  # Red
}


@beartype
def get_mechanism_plotly_data(mechanism_id: int) -> dict[str, Any]:
    """Get plotly.js compatible data for a specific mechanism chart.

    Args:
        mechanism_id: ID of the mechanism to create chart for

    Returns:
        Dictionary containing plotly.js compatible data and layout

    """
    try:
        mechanism = EnvironmentalMechanism.objects.get(id=mechanism_id)

        # Get status counts from the mechanism
        status_counts = {
            "Not Started": mechanism.not_started_count,
            "In Progress": mechanism.in_progress_count,
            "Completed": mechanism.completed_count,
            "Overdue": mechanism.overdue_count,
        }

        # Filter out zero values
        filtered_counts = {k: v for k, v in status_counts.items() if v > 0}

        if not filtered_counts:
            return {
                "data": [],
                "layout": {
                    "title": f"Mechanism: {mechanism.name}",
                    "annotations": [
                        {
                            "text": "No obligations found",
                            "x": 0.5,
                            "y": 0.5,
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                        },
                    ],
                },
            }

        # Create plotly.js data
        return {
            "data": [
                {
                    "values": list(filtered_counts.values()),
                    "labels": list(filtered_counts.keys()),
                    "type": "pie",
                    "marker": {
                        "colors": [
                            STATUS_COLORS.get(label, "#cccccc")
                            for label in filtered_counts
                        ],
                    },
                    "textinfo": "label+percent",
                    "textposition": "auto",
                    "hovertemplate": "<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": f"Mechanism: {mechanism.name}",
                    "x": 0.5,
                    "font": {"size": 16},
                },
                "margin": {"t": 60, "b": 20, "l": 20, "r": 20},
                "showlegend": True,
                "legend": {
                    "orientation": "v",
                    "x": 1.05,
                    "y": 0.5,
                },
            },
        }

    except EnvironmentalMechanism.DoesNotExist:
        logger.exception("Mechanism with ID %s does not exist", mechanism_id)
        return {
            "data": [],
            "layout": {
                "title": "Mechanism not found",
                "annotations": [
                    {
                        "text": "Mechanism not found",
                        "x": 0.5,
                        "y": 0.5,
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                    },
                ],
            },
        }
    except Exception as e:
        logger.exception("Error creating mechanism plotly data: %s", e)
        return {
            "data": [],
            "layout": {
                "title": f"Error: {e}",
                "annotations": [
                    {
                        "text": f"Error loading chart: {e}",
                        "x": 0.5,
                        "y": 0.5,
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                    },
                ],
            },
        }


@beartype
def get_overall_plotly_data(project_id: int) -> dict[str, Any]:
    """Get plotly.js compatible data for overall project mechanisms chart.

    Args:
        project_id: ID of the project to create chart for

    Returns:
        Dictionary containing plotly.js compatible data and layout

    """
    try:
        mechanisms = EnvironmentalMechanism.objects.filter(project_id=project_id)

        if not mechanisms.exists():
            return {
                "data": [],
                "layout": {
                    "title": "Overall Project Status",
                    "annotations": [
                        {
                            "text": "No mechanisms found",
                            "x": 0.5,
                            "y": 0.5,
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                        },
                    ],
                },
            }

        # Aggregate data
        not_started = sum(m.not_started_count for m in mechanisms)
        in_progress = sum(m.in_progress_count for m in mechanisms)
        completed = sum(m.completed_count for m in mechanisms)
        overdue = sum(m.overdue_count for m in mechanisms)

        status_counts = {
            "Not Started": not_started,
            "In Progress": in_progress,
            "Completed": completed,
            "Overdue": overdue,
        }

        # Filter out zero values
        filtered_counts = {k: v for k, v in status_counts.items() if v > 0}

        if not filtered_counts:
            return {
                "data": [],
                "layout": {
                    "title": "Overall Project Status",
                    "annotations": [
                        {
                            "text": "No obligations found",
                            "x": 0.5,
                            "y": 0.5,
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                        },
                    ],
                },
            }

        # Create plotly.js data
        return {
            "data": [
                {
                    "values": list(filtered_counts.values()),
                    "labels": list(filtered_counts.keys()),
                    "type": "pie",
                    "marker": {
                        "colors": [
                            STATUS_COLORS.get(label, "#cccccc")
                            for label in filtered_counts
                        ],
                    },
                    "textinfo": "label+percent",
                    "textposition": "auto",
                    "hovertemplate": "<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": "Overall Project Status",
                    "x": 0.5,
                    "font": {"size": 16},
                },
                "margin": {"t": 60, "b": 20, "l": 20, "r": 20},
                "showlegend": True,
                "legend": {
                    "orientation": "v",
                    "x": 1.05,
                    "y": 0.5,
                },
            },
        }

    except Exception as e:
        logger.exception("Error creating overall plotly data: %s", e)
        return {
            "data": [],
            "layout": {
                "title": f"Error: {e}",
                "annotations": [
                    {
                        "text": f"Error loading chart: {e}",
                        "x": 0.5,
                        "y": 0.5,
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                    },
                ],
            },
        }


@beartype
def serialize_plotly_data(data: dict[str, Any]) -> str:
    """Serialize plotly data to JSON string for client-side use.

    Args:
        data: Plotly data dictionary

    Returns:
        JSON string for use with plotly.js

    """
    try:
        return plotly.utils.PlotlyJSONEncoder().encode(data)
    except Exception as e:
        logger.exception("Error serializing plotly data: %s", e)
        return '{"data": [], "layout": {"title": "Error serializing data"}}'
