import base64
import io
import logging
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
from django.utils import timezone
from matplotlib.figure import Figure

from .models import EnvironmentalMechanism

logger = logging.getLogger(__name__)

def generate_pie_chart(data: List[int], labels: List[str], colors: List[str], fig_width: int = 300, fig_height: int = 250) -> Figure:
    """
    Generate a pie chart for given data and labels with percentages in the legend.
    """
    fig = Figure(figsize=(fig_width / 100, fig_height / 100), dpi=100)
    ax = fig.add_subplot(111)

    if sum(data) > 0:
        # Calculate percentages
        total = sum(data)
        percentages = [(value / total) * 100 for value in data]

        # Create legend labels with percentages
        legend_labels = [f"{label} ({value} - {pct:.1f}%)"
                         for label, value, pct in zip(labels, data, percentages)]

        # Create pie without percentage text on slices
        wedges, _ = ax.pie(
            data,
            colors=colors,
            startangle=90,
            labels=None,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1}
        )

        # Add legend with combined labels
        ax.legend(wedges, legend_labels, loc="best", fontsize=8, title="Status")
    else:
        ax.text(0.5, 0.5, "No data available", horizontalalignment='center', verticalalignment='center')

    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    fig.tight_layout()

    return fig

def encode_figure_to_base64(fig: Figure) -> str:
    """
    Convert a matplotlib figure to a base64 encoded string.
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def get_mechanism_chart(mechanism_id: int, fig_width: int = 300, fig_height: int = 250) -> Tuple[Figure, str]:
    """
    Get pie chart for a specific mechanism based on its statuses.
    Returns both the figure and base64 encoded image data.
    """
    try:
        mechanism = EnvironmentalMechanism.objects.get(id=mechanism_id)
        labels = ['Not Started', 'In Progress', 'Completed', 'Overdue']
        data = [
            mechanism.not_started_count,
            mechanism.in_progress_count,
            mechanism.completed_count,
            mechanism.overdue_count
        ]
        colors = ['#f9c74f', '#90be6d', '#43aa8b', '#f94144']

        fig = generate_pie_chart(data, labels, colors, fig_width, fig_height)
        encoded_image = encode_figure_to_base64(fig)
        return fig, encoded_image
    except EnvironmentalMechanism.DoesNotExist:
        logger.error(f"Mechanism with ID {mechanism_id} does not exist.")
        fig = generate_pie_chart([0, 0, 0, 0], ["None", "None", "None", "None"], ['#ccc', '#ccc', '#ccc', '#ccc'], fig_width, fig_height)
        encoded_image = encode_figure_to_base64(fig)
        return fig, encoded_image

def get_overall_chart(project_id: int, fig_width: int = 300, fig_height: int = 250) -> Tuple[Figure, str]:
    """
    Get overall pie chart for all mechanisms in a project.
    Returns both the figure and base64 encoded image data.
    """
    try:
        mechanisms = EnvironmentalMechanism.objects.filter(project_id=project_id)

        # Aggregate data
        not_started = sum(m.not_started_count for m in mechanisms)
        in_progress = sum(m.in_progress_count for m in mechanisms)
        completed = sum(m.completed_count for m in mechanisms)
        overdue = sum(m.overdue_count for m in mechanisms)

        labels = ['Not Started', 'In Progress', 'Completed', 'Overdue']
        data = [not_started, in_progress, completed, overdue]
        colors = ['#f9c74f', '#90be6d', '#43aa8b', '#f94144']

        fig = generate_pie_chart(data, labels, colors, fig_width, fig_height)
        encoded_image = encode_figure_to_base64(fig)
        return fig, encoded_image
    except Exception as e:
        logger.error(f"Error generating overall chart: {str(e)}")
        fig = generate_pie_chart([0, 0, 0, 0], ["None", "None", "None", "None"], ['#ccc', '#ccc', '#ccc', '#ccc'], fig_width, fig_height)
        encoded_image = encode_figure_to_base64(fig)
        return fig, encoded_image
