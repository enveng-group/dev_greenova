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

"""Shared chart utilities for Greenova project.

This module provides reusable functions and constants for generating charts
(e.g., pie charts) using matplotlib, to eliminate code duplication and
ensure consistent chart appearance across the project.

Author: Adrian Gallo
Email: agallo@enveng-group.com.au
License: AGPL-3.0
"""


from collections.abc import Sequence
from matplotlib.figure import Figure


def create_pie_chart(
    data: Sequence[int],
    labels: Sequence[str],
    colors: Sequence[str],
    title: str = "Status Distribution",
    fig_size: tuple[int, int] = (320, 240),
) -> Figure:
    """Create a matplotlib pie chart with consistent style for Greenova.

    Args:
        data: Sequence of values for the pie chart.
        labels: Sequence of labels for each segment.
        colors: Sequence of colors for each segment.
        title: Title for the chart.
        fig_size: Tuple of (width, height) in pixels for the figure.

    Returns:
        Matplotlib Figure object containing the pie chart.

    """
    fig_width, fig_height = fig_size
    fig: Figure = Figure(figsize=(fig_width / 100, fig_height / 100), dpi=100)
    ax = fig.add_subplot(1, 1, 1)
    if data and any(data):
        ax.pie(
            data,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={"edgecolor": "w", "linewidth": 1},
            textprops={"fontsize": 10},
        )
        ax.axis("equal")
        ax.set_title(title, fontsize=12)
    else:
        ax.text(
            0.5,
            0.5,
            "No data available",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=12,
        )
        ax.axis("off")
    fig.tight_layout()
    return fig
