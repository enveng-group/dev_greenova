"""Plotly middleware for responsibility app.

This module acts as middleware between django_matplotlib (server-side SVG) and
plotly.js (client-side interactive charts), using the plotly Python package
for data serialization and chart generation.
"""

import logging
from typing import Any

import plotly.utils
from beartype import beartype
from obligations.models import Obligation

from .figures import get_responsibility_charts_data

logger = logging.getLogger(__name__)

# Color scheme for consistency with matplotlib figures
STATUS_COLORS = {
    "Not Started": "#f9c74f",  # Yellow
    "In Progress": "#90be6d",  # Green
    "Completed": "#43aa8b",  # Teal
    "Overdue": "#f94144",  # Red
}

DEPARTMENT_COLORS = {
    "Engineering": "#3498db",  # Blue
    "Environmental": "#2ecc71",  # Green
    "Legal": "#e74c3c",  # Red
    "Management": "#f39c12",  # Orange
    "Operations": "#9b59b6",  # Purple
}


@beartype
def get_responsibility_plotly_data(project_id: int | None = None) -> dict[str, Any]:
    """Generate plotly.js data for responsibility distribution chart.

    Args:
        project_id: Optional project ID to filter obligations.

    Returns:
        Dictionary containing plotly.js compatible data and layout.

    """
    try:
        # Get responsibility charts data
        responsibility_data = get_responsibility_charts_data(project_id)

        if not responsibility_data:
            return {
                "data": [],
                "layout": {
                    "title": "Responsibility Distribution",
                    "annotations": [
                        {
                            "text": "No responsibility data found",
                            "x": 0.5,
                            "y": 0.5,
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                        },
                    ],
                },
            }

        # Extract responsibility counts
        responsibilities = list(responsibility_data.keys())
        counts = list(responsibility_data.values())

        if not responsibilities:
            return {
                "data": [],
                "layout": {
                    "title": "Responsibility Distribution",
                    "annotations": [
                        {
                            "text": "No responsibilities found",
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
                    "values": counts,
                    "labels": responsibilities,
                    "type": "pie",
                    "textinfo": "label+percent",
                    "textposition": "auto",
                    "hovertemplate": "<b>%{label}</b><br>Obligations: %{value}<br>Percentage: %{percent}<extra></extra>",
                }],
            "layout": {
                "title": {
                    "text": "Responsibility Distribution",
                    "x": 0.5,
                    "font": {
                        "size": 16},
                },
                "margin": {
                    "t": 60,
                    "b": 20,
                    "l": 20,
                    "r": 20},
                "showlegend": True,
                "legend": {
                    "orientation": "v",
                    "x": 1.05,
                    "y": 0.5,
                },
            },
        }

    except Exception as e:
        logger.exception("Error creating responsibility plotly data: %s", e)
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
def get_department_workload_plotly_data(
    project_id: int | None = None,
) -> dict[str, Any]:
    """Generate plotly.js data for department workload chart.

    Args:
        project_id: Optional project ID to filter obligations.

    Returns:
        Dictionary containing plotly.js compatible data and layout.

    """
    try:
        # Get all obligations, optionally filtered by project
        if project_id:
            obligations = Obligation.objects.filter(
                environmental_mechanism__project_id=project_id,
            )
        else:
            obligations = Obligation.objects.all()

        if not obligations.exists():
            return {
                "data": [],
                "layout": {
                    "title": "Department Workload",
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

        # Group obligations by department and status
        department_data = {}

        for obligation in obligations:
            if not obligation.responsibility:
                continue

            # Simple department extraction - in real app might be a separate field
            dept = (
                obligation.responsibility.split(" - ")[0]
                if " - " in obligation.responsibility
                else obligation.responsibility
            )

            if dept not in department_data:
                department_data[dept] = {
                    "Not Started": 0,
                    "In Progress": 0,
                    "Completed": 0,
                    "Overdue": 0,
                }

            if obligation.status == "not_started":
                department_data[dept]["Not Started"] += 1
            elif obligation.status == "in_progress":
                department_data[dept]["In Progress"] += 1
            elif obligation.status == "completed":
                department_data[dept]["Completed"] += 1

            if obligation.is_overdue:
                department_data[dept]["Overdue"] += 1

        if not department_data:
            return {
                "data": [],
                "layout": {
                    "title": "Department Workload",
                    "annotations": [
                        {
                            "text": "No department data found",
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
        departments = list(department_data.keys())
        not_started = [data["Not Started"] for data in department_data.values()]
        in_progress = [data["In Progress"] for data in department_data.values()]
        completed = [data["Completed"] for data in department_data.values()]
        overdue = [data["Overdue"] for data in department_data.values()]

        # Create plotly.js data
        return {"data": [{"x": departments,
                          "y": not_started,
                          "name": "Not Started",
                          "type": "bar",
                          "marker": {"color": STATUS_COLORS["Not Started"]},
                          "hovertemplate": "<b>%{fullData.name}</b><br>%{x}<br>Count: %{y}<extra></extra>",
                          },
                         {"x": departments,
                          "y": in_progress,
                          "name": "In Progress",
                          "type": "bar",
                          "marker": {"color": STATUS_COLORS["In Progress"]},
                          "hovertemplate": "<b>%{fullData.name}</b><br>%{x}<br>Count: %{y}<extra></extra>",
                          },
                         {"x": departments,
                          "y": completed,
                          "name": "Completed",
                          "type": "bar",
                          "marker": {"color": STATUS_COLORS["Completed"]},
                          "hovertemplate": "<b>%{fullData.name}</b><br>%{x}<br>Count: %{y}<extra></extra>",
                          },
                         {"x": departments,
                          "y": overdue,
                          "name": "Overdue",
                          "type": "bar",
                          "marker": {"color": STATUS_COLORS["Overdue"]},
                          "hovertemplate": "<b>%{fullData.name}</b><br>%{x}<br>Count: %{y}<extra></extra>",
                          },
                         ],
                "layout": {"title": {"text": "Department Workload Distribution",
                                     "x": 0.5,
                                     "font": {"size": 16},
                                     },
                           "barmode": "stack",
                           "xaxis": {"title": "Departments"},
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
        logger.exception("Error creating department workload plotly data: %s", e)
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
def get_responsibility_timeline_plotly_data(
    project_id: int | None = None,
) -> dict[str, Any]:
    """Generate plotly.js data for responsibility timeline chart.

    Args:
        project_id: Optional project ID to filter obligations.

    Returns:
        Dictionary containing plotly.js compatible data and layout.

    """
    try:
        # Get all obligations, optionally filtered by project
        if project_id:
            obligations = Obligation.objects.filter(
                environmental_mechanism__project_id=project_id,
            ).order_by("due_date")
        else:
            obligations = Obligation.objects.all().order_by("due_date")

        if not obligations.exists():
            return {
                "data": [],
                "layout": {
                    "title": "Responsibility Timeline",
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

        # Group obligations by month and responsibility
        timeline_data = {}

        for obligation in obligations:
            if not obligation.due_date or not obligation.responsibility:
                continue

            month_key = obligation.due_date.strftime("%Y-%m")

            if month_key not in timeline_data:
                timeline_data[month_key] = {}

            if obligation.responsibility not in timeline_data[month_key]:
                timeline_data[month_key][obligation.responsibility] = 0

            timeline_data[month_key][obligation.responsibility] += 1

        if not timeline_data:
            return {
                "data": [],
                "layout": {
                    "title": "Responsibility Timeline",
                    "annotations": [
                        {
                            "text": "No timeline data found",
                            "x": 0.5,
                            "y": 0.5,
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                        },
                    ],
                },
            }

        # Get all unique responsibilities
        all_responsibilities = set()
        for month_data in timeline_data.values():
            all_responsibilities.update(month_data.keys())

        # Create data series for each responsibility
        data_series = []
        colors = list(DEPARTMENT_COLORS.values())

        for i, responsibility in enumerate(sorted(all_responsibilities)):
            months = sorted(timeline_data.keys())
            counts = [timeline_data[month].get(responsibility, 0) for month in months]

            data_series.append(
                {
                    "x": months,
                    "y": counts,
                    "name": responsibility,
                    "type": "scatter",
                    "mode": "lines+markers",
                    "line": {"color": colors[i % len(colors)]},
                    "hovertemplate": f"<b>{responsibility}</b><br>Month: %{{x}}<br>Count: %{{y}}<extra></extra>",
                },
            )

        # Create plotly.js data
        return {
            "data": data_series,
            "layout": {
                "title": {
                    "text": "Responsibility Timeline",
                    "x": 0.5,
                    "font": {"size": 16},
                },
                "xaxis": {"title": "Month"},
                "yaxis": {"title": "Number of Obligations"},
                "margin": {"t": 60, "b": 60, "l": 60, "r": 20},
                "showlegend": True,
                "legend": {
                    "orientation": "v",
                    "x": 1.05,
                    "y": 0.5,
                },
            },
        }

    except Exception as e:
        logger.exception("Error creating responsibility timeline plotly data: %s", e)
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
