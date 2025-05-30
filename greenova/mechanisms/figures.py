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

"""Mechanism chart generation using plotly for interactive charts.

This module provides functions to generate interactive pie charts for environmental
mechanisms using Plotly, for integration into the Greenova dashboard.
"""

import logging
import io
from dataclasses import dataclass
from typing import Any, cast
import matplotlib as mpl
import plotly.graph_objects as go
from beartype import beartype
from core.utils.charts import create_pie_chart
from plotly.offline import plot
from .models import EnvironmentalMechanism
from . import proto_utils


# For type annotations
Figure = mpl.figure.Figure

logger = logging.getLogger(__name__)


@beartype  # type: ignore[misc]
def generate_plotly_pie_chart(
    data: list[int],
    labels: list[str],
    colors: list[str],
    mechanism_id: int | None = None,
    chart_title: str | None = None,
) -> str:
    """Generate a plotly pie chart for given data and labels.

    Args:
        data: List of values for the pie chart.
        labels: List of labels for each segment.
        colors: List of colors for each segment.
        mechanism_id: Optional mechanism ID to associate with the chart.
        chart_title: Optional title for the chart.

    Returns:
        HTML string containing the interactive plotly chart.

    """
    fig = go.Figure()

    # Prepare custom data with all necessary fields upfront
    custom_data_list: list[dict[str, Any]] = []
    for i, label_val in enumerate(labels):
        status_key = label_val.lower().replace(" ", "_")
        custom_data_list.append(
            {
                "status": label_val,
                "count": data[i],
                "mechanism_id": mechanism_id,
                "status_key": status_key,
                "color": colors[i],
            },
        )

    fig.add_trace(
        go.Pie(
            labels=labels,
            values=data,
            marker={"colors": colors},
            textinfo="percent",
            hoverinfo="label+percent+value",
            textfont={"size": 14, "color": "white"},
            customdata=custom_data_list,  # Assign the fully prepared list
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Count: %{value}<br>"
                "Percentage: %{percent:.1%}<br>"
                "<extra></extra>"
            ),
        ),
    )

    fig.update_layout(
        title=chart_title,
        margin={"l": 10, "r": 10, "t": 30, "b": 10},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": -0.1,
            "xanchor": "center",
            "x": 0.5,
        },
        autosize=True,
        height=320,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    # customdata is now fully prepared and assigned during trace creation.
    # No need for the previous loop that updated fig.data[0].customdata[i]

    # Convert to HTML with only supported arguments for plotly version
    return plot(fig, output_type="div", include_plotlyjs=False)


def encode_figure_to_svg(fig: Figure) -> str:
    """Convert a matplotlib figure to an SVG string with data attributes.

    Extracts data attributes from figure elements and adds them to the SVG output
    to enable interactive features.

    Args:
        fig: Matplotlib Figure object.

    Returns:
        SVG image as a string with data attributes preserved for interactivity.

    """
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight")
    svg_data = buf.getvalue()
    buf.close()

    # Extract data attributes from wedges and add them to the SVG
    svg_modified = svg_data

    # Find all wedge elements with gid attributes
    for wedge in fig.gca().patches:
        if hasattr(wedge, "get_gid") and wedge.get_gid():
            gid = wedge.get_gid()

            # Check for the data attributes we added to wedges
            data_attrs = {}
            if hasattr(wedge, "_data_status"):
                data_attrs["data-status"] = wedge._data_status
            if hasattr(wedge, "_data_count"):
                data_attrs["data-count"] = str(wedge._data_count)
            if hasattr(wedge, "_data_mechanism_id"):
                data_attrs["data-mechanism-id"] = wedge._data_mechanism_id
            if hasattr(wedge, "_data_status_key"):
                data_attrs["data-status-key"] = wedge._data_status_key
            if hasattr(wedge, "_data_color"):
                data_attrs["data-color"] = wedge._data_color

            # Add the attributes to the SVG
            if data_attrs:
                # Create attribute string
                attrs_str = " ".join([f'{k}="{v}"' for k, v in data_attrs.items()])

                # Find the SVG element with this gid and add the attributes
                pattern = f'id="{gid}"'
                replacement = f'id="{gid}" {attrs_str}'
                svg_modified = svg_modified.replace(pattern, replacement)

    return svg_modified


@dataclass
class PieChartParams:
    """Parameters for generating a pie chart."""

    data: list[int]
    labels: list[str]
    colors: list[str]
    mechanism_id: int | None = None
    fig_width: int = 320
    fig_height: int = 280


def get_mechanism_chart(
    mechanism_id: int, fig_width: int = 320, fig_height: int = 280,
) -> tuple[Figure, str]:
    """Get pie chart for a specific mechanism as SVG.

    Args:
        mechanism_id: The ID of the mechanism.
        fig_width: Width of the figure in pixels.
        fig_height: Height of the figure in pixels.

    Returns:
        Tuple of (matplotlib Figure, SVG image as string).

    """
    try:
        mechanism = EnvironmentalMechanism.objects.get(id=mechanism_id)
        labels = ["Not Started", "In Progress", "Completed", "Overdue"]
        data = [
            mechanism.not_started_count,
            mechanism.in_progress_count,
            mechanism.completed_count,
            mechanism.overdue_count,
        ]
        colors = ["#f9c74f", "#90be6d", "#43aa8b", "#f94144"]

        params = PieChartParams(
            data=data,
            labels=labels,
            colors=colors,
            mechanism_id=mechanism_id,
            fig_width=fig_width,
            fig_height=fig_height,
        )
        fig = generate_pie_chart(params)
        svg_image = encode_figure_to_svg(fig)
        return fig, svg_image
    except EnvironmentalMechanism.DoesNotExist:
        logger.exception("Mechanism with ID %s does not exist.", mechanism_id)
        params = PieChartParams(
            data=[0, 0, 0, 0],
            labels=["None", "None", "None", "None"],
            colors=["#ccc", "#ccc", "#ccc", "#ccc"],
            mechanism_id=None,
            fig_width=fig_width,
            fig_height=fig_height,
        )
        fig = generate_pie_chart(params)
        svg_image = encode_figure_to_svg(fig)
        return fig, svg_image


def get_overall_chart(
    project_id: int, fig_width: int = 320, fig_height: int = 280,
) -> tuple[Figure, str]:
    """Get overall pie chart for all mechanisms in a project as SVG.

    Returns both the figure and SVG image data.

    Args:
        project_id: The ID of the project.
        fig_width: Width of the figure in pixels.
        fig_height: Height of the figure in pixels.

    Returns:
        Tuple of (matplotlib Figure, SVG image as string).

    """
    try:
        mechanisms = EnvironmentalMechanism.objects.filter(project_id=project_id)

        # Aggregate data
        not_started = sum(m.not_started_count for m in mechanisms)
        in_progress = sum(m.in_progress_count for m in mechanisms)
        completed = sum(m.completed_count for m in mechanisms)
        overdue = sum(m.overdue_count for m in mechanisms)

        labels = ["Not Started", "In Progress", "Completed", "Overdue"]
        data = [not_started, in_progress, completed, overdue]
        colors = ["#f9c74f", "#90be6d", "#43aa8b", "#f94144"]

        params = PieChartParams(
            data=data,
            labels=labels,
            colors=colors,
            mechanism_id=None,
            fig_width=fig_width,
            fig_height=fig_height,
        )
        fig = generate_pie_chart(params)
        svg_image = encode_figure_to_svg(fig)
        return fig, svg_image
    except Exception as e:
        logger.exception("Error generating overall chart: %s", str(e))
        params = PieChartParams(
            data=[0, 0, 0, 0],
            labels=["None", "None", "None", "None"],
            colors=["#ccc", "#ccc", "#ccc", "#ccc"],
            mechanism_id=None,
            fig_width=fig_width,
            fig_height=fig_height,
        )
        fig = generate_pie_chart(params)
        svg_image = encode_figure_to_svg(fig)
        return fig, svg_image


@beartype  # type: ignore[misc]
def get_mechanism_plotly_chart(
    mechanism_id: int,
) -> str | None:
    """Plotly pie chart for a specific mechanism (protobuf serialization)."""
    try:
        mechanism = EnvironmentalMechanism.objects.get(id=mechanism_id)
        chart_data_pb = proto_utils.serialize_mechanism_chart_data(mechanism)

        segments = cast("list[Any]", getattr(chart_data_pb, "segments", []))
        labels: list[str] = [str(getattr(segment, "label", "")) for segment in segments]
        data: list[int] = [int(getattr(segment, "value", 0)) for segment in segments]
        colors: list[str] = [str(getattr(segment, "color", "")) for segment in segments]
        chart_html = generate_plotly_pie_chart(
            data,
            labels,
            colors,
            mechanism_id,
            mechanism.name,
        )
        return str(chart_html)
    except EnvironmentalMechanism.DoesNotExist:
        logger.exception("Mechanism with ID %s does not exist.", mechanism_id)
        return None


@beartype  # type: ignore[misc]
def get_overall_plotly_chart(
    project_id: int,
) -> str | None:
    """Plotly pie chart for all mechanisms in a project (protobuf serialization)."""
    try:
        mechanisms = EnvironmentalMechanism.objects.filter(project_id=project_id)
        chart_data_pb = proto_utils.serialize_overall_chart_data(project_id, mechanisms)
        labels = [segment.label for segment in chart_data_pb.segments]
        data = [segment.value for segment in chart_data_pb.segments]
        colors = [segment.color for segment in chart_data_pb.segments]
        chart_html = generate_plotly_pie_chart(
            data,
            labels,
            colors,
            None,
            "Overall Status",
        )
        return str(chart_html)
    except Exception as e:
        logger.exception("Error generating overall chart: %s", str(e))
        return None


@beartype  # type: ignore[misc]
def generate_pie_chart(
    params: PieChartParams,
) -> Figure:
    """Generate a static matplotlib pie chart for mechanism status.

    Args:
        params: PieChartParams dataclass containing chart parameters.

    Returns:
        Matplotlib Figure object containing the pie chart.

    """
    # Prepare custom data attributes for wedges (optional, for SVG interactivity)
    data_attrs: list[dict[str, object]] = []
    for i, value in enumerate(params.data):
        data_attrs.append(
            {
                "_data_status": params.labels[i] if i < len(params.labels) else "",
                "_data_count": value,
                "_data_mechanism_id": params.mechanism_id
                if params.mechanism_id is not None
                else "",
                "_data_status_key": params.labels[i].lower().replace(" ", "_")
                if i < len(params.labels)
                else "",
                "_data_color": params.colors[i] if i < len(params.colors) else "",
            },
        )
    return create_pie_chart(
        data=params.data,
        labels=params.labels,
        colors=params.colors,
        title="Status Distribution",
    )
