from typing import Dict, List, Optional, Union
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.figure import Figure
from django.utils import timezone
import logging
from .models import EnvironmentalMechanism

logger = logging.getLogger(__name__)

def get_mechanism_chart(mechanism_id: int, fig_width: int = 300, fig_height: int = 250) -> plt.Figure:
    """
    Generate a pie chart for a specific mechanism's obligation statuses.
    """
    try:
        # Get the mechanism
        mechanism = EnvironmentalMechanism.objects.get(id=mechanism_id)

        # Prepare status data
        labels = ['Not Started', 'In Progress', 'Completed', 'Overdue']
        sizes = [
            mechanism.not_started_count,
            mechanism.in_progress_count,
            mechanism.completed_count,
            mechanism.overdue_count
        ]
        colors = ['#f9c74f', '#90be6d', '#43aa8b', '#f94144']

        # Create figure and plot
        fig = Figure(figsize=(fig_width/100, fig_height/100), dpi=100)
        ax = fig.add_subplot(111)

        # Only plot if there's data
        if sum(sizes) > 0:
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        else:
            ax.text(0.5, 0.5, 'No obligations', horizontalalignment='center', verticalalignment='center')

        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        fig.tight_layout()

        return fig

    except Exception as e:
        logger.error(f"Error generating mechanism chart: {str(e)}")
        # Return a simple error figure
        fig = Figure(figsize=(fig_width/100, fig_height/100), dpi=100)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, f"Error: {str(e)}", horizontalalignment='center', verticalalignment='center')
        return fig

def get_overall_chart(project_id: int, fig_width: int = 300, fig_height: int = 250) -> plt.Figure:
    """
    Generate an overall pie chart for all mechanisms in a project.
    """
    try:
        # Get all mechanisms for this project
        mechanisms = EnvironmentalMechanism.objects.filter(project_id=project_id)

        # Sum up all status counts
        not_started = sum(m.not_started_count for m in mechanisms)
        in_progress = sum(m.in_progress_count for m in mechanisms)
        completed = sum(m.completed_count for m in mechanisms)
        overdue = sum(m.overdue_count for m in mechanisms)

        # Prepare chart data
        labels = ['Not Started', 'In Progress', 'Completed', 'Overdue']
        sizes = [not_started, in_progress, completed, overdue]
        colors = ['#f9c74f', '#90be6d', '#43aa8b', '#f94144']

        # Create figure
        fig = Figure(figsize=(fig_width/100, fig_height/100), dpi=100)
        ax = fig.add_subplot(111)

        # Only plot if there's data
        if sum(sizes) > 0:
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        else:
            ax.text(0.5, 0.5, 'No obligations', horizontalalignment='center', verticalalignment='center')

        ax.axis('equal')
        fig.tight_layout()

        return fig

    except Exception as e:
        logger.error(f"Error generating overall chart: {str(e)}")
        # Return a simple error figure
        fig = Figure(figsize=(fig_width/100, fig_height/100), dpi=100)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, f"Error: {str(e)}", horizontalalignment='center', verticalalignment='center')
        return fig
