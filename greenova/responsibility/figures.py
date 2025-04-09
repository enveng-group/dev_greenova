import logging
from typing import Dict, List, Optional, Union

import matplotlib
import matplotlib.pyplot as plt
from django.db.models import Count
from matplotlib.figure import Figure
from obligations.models import Obligation

logger = logging.getLogger(__name__)

def generate_responsibility_chart(responsibility_counts: Dict[str, int], fig_width: int = 600, fig_height: int = 300) -> Figure:
    """
    Generate a horizontal bar chart showing obligation counts by responsibility.

    Args:
        responsibility_counts: Dictionary mapping responsibility names to counts
        fig_width: Width of figure in pixels
        fig_height: Height of figure in pixels

    Returns:
        A matplotlib Figure with the horizontal bar chart
    """
    try:
        # Extract responsibility labels and counts
        labels = list(responsibility_counts.keys())
        counts = list(responsibility_counts.values())

        # Create figure with appropriate size
        fig = Figure(figsize=(fig_width / 100, fig_height / 100), dpi=100)
        ax = fig.add_subplot(111)

        # Only plot if we have data
        if labels:
            # Create horizontal bar chart
            y_pos = range(len(labels))
            bars = ax.barh(y_pos, counts, align='center', color='#65a879')
            ax.set_yticks(y_pos)
            ax.set_yticklabels(labels)
            ax.invert_yaxis()  # Labels read top-to-bottom
            ax.set_xlabel('Number of Obligations')

            # Add count labels to the right of each bar
            for i, v in enumerate(counts):
                ax.text(v + 0.1, i, str(v), va='center')

            # Set title with accessible font size
            ax.set_title('Obligations by Responsibility', fontsize=12)
        else:
            ax.text(0.5, 0.5, 'No data available',
                    horizontalalignment='center',
                    verticalalignment='center')

        # Ensure proper layout with enough room for labels
        fig.tight_layout()
        return fig

    except Exception as e:
        logger.error(f'Error generating responsibility chart: {str(e)}')
        # Return a simple error figure
        fig = Figure(figsize=(fig_width / 100, fig_height / 100), dpi=100)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, f'Error: {str(e)}', horizontalalignment='center', verticalalignment='center')
        return fig


# Keep the original function with correct implementation
def get_responsibility_chart(mechanism_id: int, fig_width: int = 600, fig_height: int = 300, filtered_ids: Optional[List[int]] = None) -> Figure:
    """
    Generate a horizontal bar chart showing obligation counts by responsibility.

    Args:
        mechanism_id: ID of the environmental mechanism to filter by
        fig_width: Width of figure in pixels
        fig_height: Height of figure in pixels
        filtered_ids: Optional list of obligation IDs to filter by

    Returns:
        A matplotlib Figure with the horizontal bar chart
    """
    try:
        # Get obligations for this mechanism
        obligations = Obligation.objects.filter(primary_environmental_mechanism_id=mechanism_id)

        # Apply additional filtering if provided
        if filtered_ids is not None:
            obligations = obligations.filter(id__in=filtered_ids)

        # Count obligations by responsibility using the ORM
        responsibility_data = obligations.values('responsibility').annotate(
            count=Count('obligation_number')
        ).order_by('-count')

        # Extract responsibility labels and counts
        labels = [item['responsibility'] for item in responsibility_data]
        counts = [item['count'] for item in responsibility_data]

        # Create figure with appropriate size
        fig = Figure(figsize=(fig_width / 100, fig_height / 100), dpi=100)
        ax = fig.add_subplot(111)

        # Only plot if we have data
        if labels:
            # Create horizontal bar chart
            y_pos = range(len(labels))
            bars = ax.barh(y_pos, counts, align='center', color='#65a879')
            ax.set_yticks(y_pos)
            ax.set_yticklabels(labels)
            ax.invert_yaxis()  # Labels read top-to-bottom
            ax.set_xlabel('Number of Obligations')

            # Add count labels to the right of each bar
            for i, v in enumerate(counts):
                ax.text(v + 0.1, i, str(v), va='center')

            # Set title with accessible font size
            ax.set_title('Obligations by Responsibility', fontsize=12)
        else:
            ax.text(0.5, 0.5, 'No data available',
                    horizontalalignment='center',
                    verticalalignment='center')

        # Ensure proper layout with enough room for labels
        fig.tight_layout()
        return fig

    except Exception as e:
        logger.error(f'Error generating responsibility chart: {str(e)}')
        # Return a simple error figure
        fig = Figure(figsize=(fig_width / 100, fig_height / 100), dpi=100)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, f'Error: {str(e)}', horizontalalignment='center', verticalalignment='center')
        return fig
