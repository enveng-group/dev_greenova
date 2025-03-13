from typing import Dict, List, Optional, Union
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from django.db.models import Count, Q
from django.utils import timezone
import logging
from obligations.models import Obligation
from obligations.utils import is_obligation_overdue

logger = logging.getLogger(__name__)

def get_procedure_chart(procedure_name: str, mechanism_id: Optional[int] = None,
                        fig_width: int = 300, fig_height: int = 250,
                        filtered_ids: Optional[List[int]] = None) -> plt.Figure:
    """
    Generate a pie chart for a specific procedure's obligation statuses.

    Args:
        procedure_name: The name of the procedure to chart
        mechanism_id: Optional filter by environmental mechanism
        fig_width: Width of figure in pixels
        fig_height: Height of figure in pixels
        filtered_ids: Optional list of obligation IDs to filter by

    Returns:
        A matplotlib Figure object with the chart
    """
    try:
        # Start with base query
        query = Obligation.objects.filter(procedure=procedure_name)

        # Add mechanism filter if provided
        if mechanism_id:
            query = query.filter(primary_environmental_mechanism_id=mechanism_id)

        # Add filtered IDs if provided
        if filtered_ids is not None:
            query = query.filter(id__in=filtered_ids)

        # Get all obligations for this procedure
        obligations = list(query)

        # Count statuses
        not_started = 0
        in_progress = 0
        completed = 0
        overdue = 0

        for obligation in obligations:
            if obligation.status == 'completed':
                completed += 1
            elif obligation.status == 'in progress':
                in_progress += 1
            elif obligation.status == 'not started':
                not_started += 1

            # Check if overdue using utility function
            if is_obligation_overdue(obligation):
                overdue += 1
                # Adjust not_started count since overdue is a separate category
                if obligation.status == 'not started':
                    not_started -= 1

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

        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        fig.tight_layout()

        return fig

    except Exception as e:
        logger.error(f"Error generating procedure chart: {str(e)}")
        # Return a simple error figure
        fig = Figure(figsize=(fig_width/100, fig_height/100), dpi=100)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, f"Error: {str(e)}", horizontalalignment='center', verticalalignment='center')
        return fig

def get_all_procedure_charts(mechanism_id: int, fig_width: int = 300, fig_height: int = 250,
                             filtered_ids: Optional[List[int]] = None) -> Dict[str, plt.Figure]:
    """
    Generate charts for all procedures used within a specific mechanism.

    Args:
        mechanism_id: ID of the environmental mechanism to filter by
        fig_width: Width of figure in pixels
        fig_height: Height of figure in pixels
        filtered_ids: Optional list of obligation IDs to filter by

    Returns:
        Dictionary mapping procedure names to matplotlib figures
    """
    charts = {}

    try:
        # Get all distinct procedures used in this mechanism
        base_query = Obligation.objects.filter(primary_environmental_mechanism_id=mechanism_id)
        if filtered_ids is not None:
            base_query = base_query.filter(id__in=filtered_ids)

        procedures = base_query.values_list('procedure', flat=True).distinct()

        # Generate a chart for each procedure
        for procedure in procedures:
            if procedure:  # Skip None values
                charts[procedure] = get_procedure_chart(
                    procedure, mechanism_id, fig_width, fig_height, filtered_ids
                )

    except Exception as e:
        logger.error(f"Error generating procedure charts: {str(e)}")

    return charts
