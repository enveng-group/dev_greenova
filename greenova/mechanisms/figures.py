from typing import Dict, List
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from django.utils import timezone
import logging
from .models import EnvironmentalMechanism

logger = logging.getLogger(__name__)

def generate_pie_chart(data: List[int], labels: List[str], colors: List[str], fig_width: int = 300, fig_height: int = 250) -> Figure:
    """
    Generate a pie chart for given data and labels.
    """
    fig = Figure(figsize=(fig_width / 100, fig_height / 100), dpi=100)
    ax = fig.add_subplot(111)

    if sum(data) > 0:
        wedges, texts, autotexts = ax.pie(
            data,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            labels=None
        )
        ax.legend(wedges, labels, loc="best", fontsize=8)
        for autotext in autotexts:
            autotext.set_fontsize(8)
    else:
        ax.text(0.5, 0.5, "No data available", horizontalalignment='center', verticalalignment='center')

    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    fig.tight_layout()

    return fig

def get_mechanism_chart(mechanism_id: int, fig_width: int = 300, fig_height: int = 250) -> Figure:
    """
    Get pie chart for a specific mechanism based on its statuses.
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

        return generate_pie_chart(data, labels, colors, fig_width, fig_height)
    except EnvironmentalMechanism.DoesNotExist:
        logger.error(f"Mechanism with ID {mechanism_id} does not exist.")
        return generate_pie_chart([0, 0, 0, 0], ["None", "None", "None", "None"], ['#ccc', '#ccc', '#ccc', '#ccc'], fig_width, fig_height)

def get_overall_chart(project_id: int, fig_width: int = 300, fig_height: int = 250) -> Figure:
    """
    Get overall pie chart for all mechanisms in a project.
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

        return generate_pie_chart(data, labels, colors, fig_width, fig_height)
    except Exception as e:
        logger.error(f"Error generating overall chart: {str(e)}")
        return generate_pie_chart([0, 0, 0, 0], ["None", "None", "None", "None"], ['#ccc', '#ccc', '#ccc', '#ccc'], fig_width, fig_height)
