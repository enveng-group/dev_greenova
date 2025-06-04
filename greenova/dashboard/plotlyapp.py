"""Plotly middleware for dashboard app.

This module acts as middleware between django_matplotlib (server-side SVG) and
plotly.js (client-side interactive charts), using the plotly Python package
for data serialization and chart generation.
"""

import logging
from typing import Any

import plotly.utils
from beartype import beartype

from .commons import STATUS_COLORS
from .figures import (
    get_completion_trends_data,
    get_dashboard_stats,
    get_mechanism_status_data,
)

logger = logging.getLogger(__name__)


@beartype
def get_dashboard_overview_plotly_data(project_id: str | None = None) -> dict[str, Any]:
    """Generate plotly.js data for dashboard overview chart.

    Args:
        project_id: Optional project ID to filter obligations.

    Returns:
        Dictionary containing plotly.js compatible data and layout.

    """
    try:
        # Get dashboard statistics
        stats = get_dashboard_stats(project_id)

        if not stats or stats.get("total_obligations", 0) == 0:
            return {
                "data": [],
                "layout": {
                    "title": "Dashboard Overview",
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

        # Extract status counts
        status_counts = {
            "Not Started": stats.get("not_started", 0),
            "In Progress": stats.get("in_progress", 0),
            "Completed": stats.get("completed", 0),
            "Overdue": stats.get("overdue", 0),
        }

        # Filter out zero values
        filtered_counts = {k: v for k, v in status_counts.items() if v > 0}

        if not filtered_counts:
            return {
                "data": [],
                "layout": {
                    "title": "Dashboard Overview",
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
                    "text": "Overall Status Distribution",
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
        logger.exception("Error creating dashboard overview plotly data: %s", e)
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
def get_mechanism_status_plotly_data(project_id: str | None = None) -> dict[str, Any]:
    """Generate plotly.js data for mechanism status chart.

    Args:
        project_id: Optional project ID to filter mechanisms.

    Returns:
        Dictionary containing plotly.js compatible data and layout.

    """
    try:
        # Get mechanism status data
        mechanism_data = get_mechanism_status_data(project_id)

        if not mechanism_data:
            return {
                "data": [],
                "layout": {
                    "title": "Mechanism Status Distribution",
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

        # Prepare data for stacked bar chart
        mechanisms = list(mechanism_data.keys())
        not_started = [data["not_started"] for data in mechanism_data.values()]
        in_progress = [data["in_progress"] for data in mechanism_data.values()]
        completed = [data["completed"] for data in mechanism_data.values()]
        overdue = [data["overdue"] for data in mechanism_data.values()]

        # Create plotly.js data
        return {"data": [{"x": mechanisms,
                          "y": not_started,
                          "name": "Not Started",
                          "type": "bar",
                          "marker": {"color": STATUS_COLORS["Not Started"]},
                          "hovertemplate": "<b>%{fullData.name}</b><br>%{x}<br>Count: %{y}<extra></extra>",
                          },
                         {"x": mechanisms,
                          "y": in_progress,
                          "name": "In Progress",
                          "type": "bar",
                          "marker": {"color": STATUS_COLORS["In Progress"]},
                          "hovertemplate": "<b>%{fullData.name}</b><br>%{x}<br>Count: %{y}<extra></extra>",
                          },
                         {"x": mechanisms,
                          "y": completed,
                          "name": "Completed",
                          "type": "bar",
                          "marker": {"color": STATUS_COLORS["Completed"]},
                          "hovertemplate": "<b>%{fullData.name}</b><br>%{x}<br>Count: %{y}<extra></extra>",
                          },
                         {"x": mechanisms,
                          "y": overdue,
                          "name": "Overdue",
                          "type": "bar",
                          "marker": {"color": STATUS_COLORS["Overdue"]},
                          "hovertemplate": "<b>%{fullData.name}</b><br>%{x}<br>Count: %{y}<extra></extra>",
                          },
                         ],
                "layout": {"title": {"text": "Mechanism Status Distribution",
                                     "x": 0.5,
                                     "font": {"size": 16},
                                     },
                           "barmode": "stack",
                           "xaxis": {"title": "Environmental Mechanisms"},
                           "yaxis": {"title": "Number of Obligations"},
                           "margin": {"t": 60,
                                      "b": 100,
                                      "l": 60,
                                      "r": 20},
                           "showlegend": True,
                           "legend": {"orientation": "h",
                                      "x": 0.5,
                                      "xanchor": "center",
                                      "y": -0.2,
                                      },
                           },
                }

    except Exception as e:
        logger.exception("Error creating mechanism status plotly data: %s", e)
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
def get_completion_trends_plotly_data(project_id: str | None = None) -> dict[str, Any]:
    """Generate plotly.js data for completion trends chart.

    Args:
        project_id: Optional project ID to filter obligations.

    Returns:
        Dictionary containing plotly.js compatible data and layout.

    """
    try:
        # Get completion trends data
        trends_data = get_completion_trends_data(project_id)

        if not trends_data:
            return {
                "data": [],
                "layout": {
                    "title": "Completion Trends",
                    "annotations": [
                        {
                            "text": "No trend data available",
                            "x": 0.5,
                            "y": 0.5,
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                        },
                    ],
                },
            }

        # Extract dates and completion rates
        dates = [item["date"] for item in trends_data]
        completion_rates = [item["completion_rate"] for item in trends_data]

        # Create plotly.js data
        return {
            "data": [
                {
                    "x": dates,
                    "y": completion_rates,
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": "Completion Rate",
                    "line": {"color": STATUS_COLORS["Completed"], "width": 3},
                    "marker": {"size": 8},
                    "hovertemplate": "<b>Completion Rate</b><br>Date: %{x}<br>Rate: %{y:.1f}%<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": "Completion Trends Over Time",
                    "x": 0.5,
                    "font": {"size": 16},
                },
                "xaxis": {"title": "Date"},
                "yaxis": {"title": "Completion Rate (%)", "range": [0, 100]},
                "margin": {"t": 60, "b": 60, "l": 60, "r": 20},
                "showlegend": False,
            },
        }

    except Exception as e:
        logger.exception("Error creating completion trends plotly data: %s", e)
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
    """Serialize plotly data to JSON string for use in templates.

    Args:
        data: Plotly data dictionary.

    Returns:
        JSON string representation of the data.

    """
    try:
        return plotly.utils.PlotlyJSONEncoder().encode(data)
    except Exception as e:
        logger.exception("Error serializing plotly data: %s", e)
        return "{}"
