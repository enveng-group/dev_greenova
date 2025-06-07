"""Figure generation utilities for mechanisms.

This module provides functions to generate charts and figures for mechanisms
using matplotlib and plotly.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import base64
import io
import logging

from beartype import beartype
from core.constants import MECHANISM_STATUS_COLORS
from matplotlib.figure import Figure

from .models import EnvironmentalMechanism

logger = logging.getLogger(__name__)


@beartype
def generate_pie_chart(
    data: list[int],
    labels: list[str],
    colors: list[str],
    fig_width: int = 300,
    fig_height: int = 250,
) -> Figure:  # type: ignore[name-defined]
    """Generate a pie chart for given data and labels with percentages in the
    legend.

    Args:
        data: List of values for the pie chart.
        labels: List of labels for each segment.
        colors: List of colors for each segment.
        fig_width: Width of the figure in pixels.
        fig_height: Height of the figure in pixels.

    Returns:
        Matplotlib Figure object.

    """
    fig: Figure = Figure(
        figsize=(
            fig_width / 100,
            fig_height / 100),
        dpi=100)  # type: ignore[name-defined]
    ax = fig.add_subplot(111)

    if sum(data) > 0:
        # Calculate percentages
        total: int = sum(data)
        percentages: list[float] = [(value / total) * 100 for value in data]

        # Create legend labels with percentages
        legend_labels: list[str] = [
            f"{label} ({value} - {pct:.1f}%)"
            for label, value, pct in zip(labels, data, percentages, strict=False)
        ]

        # Create pie without percentage text on slices
        wedges, _ = ax.pie(
            data,
            colors=colors,
            startangle=90,
            labels=None,
            wedgeprops={"edgecolor": "white", "linewidth": 1},
        )

        # Add legend with combined labels
        ax.legend(wedges, legend_labels, loc="best", fontsize=8, title="Status")
    else:
        ax.text(
            0.5,
            0.5,
            "No data available",
            horizontalalignment="center",
            verticalalignment="center",
        )

    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle
    fig.tight_layout()

    return fig


@beartype
def encode_figure_to_base64(fig: Figure) -> str:  # type: ignore[name-defined]
    """Convert a matplotlib figure to a base64 encoded string.

    Args:
        fig: Matplotlib Figure object.

    Returns:
        Base64 encoded PNG image string.

    """
    buf: io.BytesIO = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


@beartype
def get_mechanism_chart(
    mechanism_id: int,
    fig_width: int = 300,
    fig_height: int = 250,
) -> tuple[Figure, str]:  # type: ignore[name-defined]
    """Generate a chart and base64 image for a specific mechanism.

    Args:
        mechanism_id: ID of the mechanism.
        fig_width: Width of the figure in pixels.
        fig_height: Height of the figure in pixels.

    Returns:
        Tuple of (Figure, base64 image string).

    """
    try:
        mechanism: EnvironmentalMechanism = EnvironmentalMechanism.objects.get(
            id=mechanism_id,
        )
        labels: list[str] = ["Not Started", "In Progress", "Completed", "Overdue"]
        data: list[int] = [
            mechanism.not_started_count,
            mechanism.in_progress_count,
            mechanism.completed_count,
            mechanism.overdue_count,
        ]
        colors: list[str] = list(MECHANISM_STATUS_COLORS.values())

        fig: Figure = generate_pie_chart(data, labels, colors, fig_width, fig_height)
        encoded_image: str = encode_figure_to_base64(fig)
        return fig, encoded_image
    except EnvironmentalMechanism.DoesNotExist:
        logger.exception("Mechanism with ID %s does not exist.", mechanism_id)
        fig: Figure = generate_pie_chart(
            [0, 0, 0, 0],
            ["None", "None", "None", "None"],
            ["#ccc", "#ccc", "#ccc", "#ccc"],
            fig_width,
            fig_height,
        )
        encoded_image: str = encode_figure_to_base64(fig)
        return fig, encoded_image


@beartype
def get_overall_chart(
    project_id: int,
    fig_width: int = 300,
    fig_height: int = 250,
) -> tuple[Figure, str]:  # type: ignore[name-defined]
    """Generate an overall chart and base64 image for all mechanisms in a
    project.

    Args:
        project_id: ID of the project.
        fig_width: Width of the figure in pixels.
        fig_height: Height of the figure in pixels.

    Returns:
        Tuple of (Figure, base64 image string).

    """
    try:
        mechanisms: list[EnvironmentalMechanism] = (
            EnvironmentalMechanism.objects.filter(project_id=project_id)
        )

        # Aggregate data
        not_started: int = sum(m.not_started_count for m in mechanisms)
        in_progress: int = sum(m.in_progress_count for m in mechanisms)
        completed: int = sum(m.completed_count for m in mechanisms)
        overdue: int = sum(m.overdue_count for m in mechanisms)

        labels: list[str] = ["Not Started", "In Progress", "Completed", "Overdue"]
        data: list[int] = [not_started, in_progress, completed, overdue]
        colors: list[str] = list(MECHANISM_STATUS_COLORS.values())

        fig: Figure = generate_pie_chart(data, labels, colors, fig_width, fig_height)
        encoded_image: str = encode_figure_to_base64(fig)
        return fig, encoded_image
    except Exception as e:
        logger.exception("Error generating overall chart: %s", str(e))
        fig: Figure = generate_pie_chart(
            [0, 0, 0, 0],
            ["None", "None", "None", "None"],
            ["#ccc", "#ccc", "#ccc", "#ccc"],
            fig_width,
            fig_height,
        )
        encoded_image: str = encode_figure_to_base64(fig)
        return fig, encoded_image


@beartype
def generate_mechanism_figure(data: dict[str, Any]) -> Any:
    """Generate a mechanism figure from provided data.

    Args:
        data: Dictionary containing mechanism data for plotting.

    Returns:
        A matplotlib or plotly figure object.

    """
