"""Plotly middleware for procedures app.

This module acts as middleware between django_matplotlib (server-side SVG) and
plotly.js (client-side interactive charts), using the plotly Python package
for data serialization and chart generation.
"""

import logging
from typing import Any

import plotly.utils
from beartype import beartype
from mechanisms.models import EnvironmentalMechanism
from obligations.models import Obligation

logger = logging.getLogger(__name__)

# Color scheme for consistency with matplotlib figures
STATUS_COLORS = {
    "Not Started": "#f9c74f",  # Yellow
    "In Progress": "#90be6d",  # Green
    "Completed": "#43aa8b",  # Teal
    "Overdue": "#f94144",  # Red
}


@beartype
def get_procedure_plotly_data(mechanism_id: int, procedure_name: str) -> dict[str, Any]:
    """Generate plotly.js data for a specific procedure chart.

    Args:
        mechanism_id: ID of the environmental mechanism.
        procedure_name: Name of the procedure.

    Returns:
        Dictionary containing plotly.js compatible data and layout.

    """
    try:
        EnvironmentalMechanism.objects.get(id=mechanism_id)

        # Get obligations for this specific procedure
        obligations = Obligation.objects.filter(
            environmental_mechanism_id=mechanism_id,
            procedure=procedure_name,
        )

        if not obligations.exists():
            return {
                "data": [],
                "layout": {
                    "title": f"Procedure: {procedure_name}",
                    "annotations": [
                        {
                            "text": "No obligations found for this procedure",
                            "x": 0.5,
                            "y": 0.5,
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                        },
                    ],
                },
            }

        # Calculate status counts
        not_started = obligations.filter(status="not_started").count()
        in_progress = obligations.filter(status="in_progress").count()
        completed = obligations.filter(status="completed").count()
        overdue = sum(1 for o in obligations if o.is_overdue)

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
                    "title": f"Procedure: {procedure_name}",
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
                    "text": f"Procedure: {procedure_name}",
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
        logger.exception("Error creating procedure plotly data: %s", e)
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
def get_all_procedures_plotly_data(mechanism_id: int) -> dict[str, Any]:
    """Generate plotly.js data for all procedures overview chart.

    Args:
        mechanism_id: ID of the environmental mechanism.

    Returns:
        Dictionary containing plotly.js compatible data and layout.

    """
    try:
        mechanism = EnvironmentalMechanism.objects.get(id=mechanism_id)

        # Get all obligations for this mechanism
        obligations = Obligation.objects.filter(environmental_mechanism_id=mechanism_id)

        if not obligations.exists():
            return {
                "data": [],
                "layout": {
                    "title": "All Procedures Overview",
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

        # Group by procedure and count statuses
        procedure_data = {}
        procedures = obligations.values_list("procedure", flat=True).distinct()

        for procedure in procedures:
            if not procedure:
                continue

            proc_obligations = obligations.filter(procedure=procedure)
            not_started = proc_obligations.filter(status="not_started").count()
            in_progress = proc_obligations.filter(status="in_progress").count()
            completed = proc_obligations.filter(status="completed").count()
            sum(1 for o in proc_obligations if o.is_overdue)

            total = not_started + in_progress + completed
            procedure_data[procedure] = total

        if not procedure_data:
            return {
                "data": [],
                "layout": {
                    "title": "All Procedures Overview",
                    "annotations": [
                        {
                            "text": "No procedures found",
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
                    "values": list(procedure_data.values()),
                    "labels": list(procedure_data.keys()),
                    "type": "pie",
                    "textinfo": "label+percent",
                    "textposition": "auto",
                    "hovertemplate": "<b>%{label}</b><br>Obligations: %{value}<br>Percentage: %{percent}<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": f"All Procedures Overview - {mechanism.name}",
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
        logger.exception("Error creating all procedures plotly data: %s", e)
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
