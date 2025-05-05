"""Module for generating figures and statistics for procedures."""
import io
import logging
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from django.db.models import Count, F, Q, QuerySet, Sum
from matplotlib.axes import Axes
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from obligations.models import Obligation
from procedures.models import Procedure
from projects.models import Project

matplotlib.use('Agg')

logger = logging.getLogger(__name__)

def generate_procedure_statistics(
    project_slug: Optional[str] = None
) -> Tuple[Figure, Dict[str, Any]]:
    """Generate statistics and matplotlib figure for procedures."""
    proc_query_params: Dict[str, Any] = {}
    if project_slug:
        try:
            project = Project.objects.get(slug=project_slug)
            proc_query_params['project'] = project
        except Project.DoesNotExist:
            logger.warning("Project with slug %s not found", project_slug)

    procedures = Procedure.objects.filter(**proc_query_params)
    stats = _calculate_procedure_statistics(procedures)

    fig_config = {
        'figsize': (10, 8),
        'dpi': 100,
        'facecolor': '#f9f9f9',
        'edgecolor': '#eeeeee',
    }

    fig, axes = plt.subplots(
        nrows=2,
        ncols=1,
        squeeze=True,
        figsize=fig_config['figsize'],
        dpi=fig_config['dpi'],
        facecolor=fig_config['facecolor'],
        edgecolor=fig_config['edgecolor']
    )
    axes_array = cast(np.ndarray, axes)

    try:
        if len(axes_array) >= 2:
            _plot_procedure_status_chart(cast(Axes, axes_array[0]), stats)
            _plot_procedure_timeline_chart(cast(Axes, axes_array[1]), stats)
        else:
            logger.error("Not enough axes created for plotting charts")
            plt.close(fig)
            raise ValueError("Failed to create required chart axes")
    except (IndexError, ValueError) as e:
        logger.error("Error plotting procedure charts: %s", str(e))
        plt.close(fig)
        raise
    except Exception as e:
        logger.error("Unexpected error in chart generation: %s", str(e))
        plt.close(fig)
        raise

    plt.tight_layout()
    return fig, stats


def _calculate_procedure_statistics(procedures: QuerySet) -> Dict[str, Any]:
    """Calculate statistics from procedures queryset."""
    status_counts = procedures.values('status').annotate(
        count=Sum('id', distinct=True)
    ).order_by('status')

    timeline_data = procedures.values('created_at__month').annotate(
        count=Sum('id', distinct=True),
        month=F('created_at__month')
    ).order_by('created_at__month')

    return {
        'total_count': procedures.count(),
        'status_counts': list(status_counts),
        'timeline_data': list(timeline_data)
    }


def _plot_procedure_status_chart(ax: Axes, stats: Dict[str, Any]) -> None:
    """Plot procedure status distribution chart."""
    status_labels = [item['status'] or 'Unknown' for item in stats['status_counts']]
    status_values = [item['count'] for item in stats['status_counts']]
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']

    ax.bar(status_labels, status_values, color=colors)
    ax.set_title('Procedure Status Distribution')
    ax.set_xlabel('Status')
    ax.set_ylabel('Count')
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    for i, v in enumerate(status_values):
        ax.text(i, v + 0.1, str(v), ha='center')


def _plot_procedure_timeline_chart(ax: Axes, stats: Dict[str, Any]) -> None:
    """Plot procedure timeline chart."""
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    timeline_months = [month_names[item['month'] - 1]
                       for item in stats['timeline_data']]
    timeline_counts = [item['count'] for item in stats['timeline_data']]

    ax.plot(timeline_months, timeline_counts, marker='o',
            linestyle='-', color='#3498db', linewidth=2)
    ax.set_title('Procedures Created Over Time')
    ax.set_xlabel('Month')
    ax.set_ylabel('Count')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))


def get_procedure_charts(
    mechanism_id: Union[str, int],
    filtered_ids: Optional[List[int]] = None
) -> Dict[str, Figure]:
    """Generate charts for procedures related to an environmental mechanism."""
    procedure_charts: Dict[str, Figure] = {}

    try:
        query = Obligation.objects.filter(
            primary_environmental_mechanism_id=mechanism_id
        )

        if filtered_ids is not None:
            query = query.filter(id__in=filtered_ids)

        proc_names = query.values_list('procedure', flat=True).distinct().order_by(
            'procedure'
        )

        for proc_name in proc_names:
            if not proc_name:
                continue

            proc_obligations = query.filter(procedure=proc_name)
            status_counts = _get_status_counts(proc_obligations)

            if sum(status_counts.values()) > 0:
                fig = _create_pie_chart(proc_name, status_counts)
            else:
                fig = _create_empty_chart(proc_name)

            procedure_charts[proc_name] = fig

    except (Obligation.DoesNotExist, ValueError, TypeError) as e:
        logger.error("Error generating procedure charts: %s", str(e))
        fig = _create_error_chart(str(e))
        procedure_charts["Error"] = fig

    return procedure_charts


def _get_status_counts(obligations: QuerySet) -> Dict[str, int]:
    """Get counts of obligations by status."""
    return {
        'Not Started': obligations.filter(status='not started').count(),
        'In Progress': obligations.filter(status='in progress').count(),
        'Completed': obligations.filter(status='completed').count()
    }


def _create_pie_chart(title: str, status_counts: Dict[str, int]) -> Figure:
    """Create a pie chart for procedure status distribution."""
    fig, ax = plt.subplots(figsize=(6, 5))

    labels = list(status_counts.keys())
    sizes = list(status_counts.values())
    colors = ['#f39c12', '#3498db', '#2ecc71']

    ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'w', 'linewidth': 1},
        textprops={'fontsize': 10}
    )

    ax.axis('equal')
    ax.set_title(f"{title} Status", fontsize=12)
    return fig


def _create_empty_chart(title: str) -> Figure:
    """Create an empty chart with a message."""
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.text(
        0.5, 0.5,
        "No obligations found",
        ha='center',
        va='center',
        fontsize=12
    )
    ax.axis('off')
    ax.set_title(title, fontsize=12)
    return fig


def _create_error_chart(error_message: str) -> Figure:
    """Create an error chart with the error message."""
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.text(
        0.5, 0.5,
        f"Error generating charts: {error_message}",
        ha='center',
        va='center',
        fontsize=10,
        wrap=True
    )
    ax.axis('off')
    return fig


def get_all_procedure_charts() -> Dict[str, bytes]:
    """Generate all procedure charts and return them as a dictionary.

    Returns:
        Dict[str, bytes]: Dictionary mapping chart names to PNG image data.
    """
    # Initialize dictionary to store charts
    charts = {}

    # Get procedure status distribution chart
    status_chart = get_procedure_status_chart()
    charts['status_distribution'] = chart_to_png(status_chart)

    # Get procedure timeline chart
    timeline_chart = get_procedure_timeline()
    charts['timeline'] = chart_to_png(timeline_chart)

    # Get procedure completion rate chart
    completion_chart = get_completion_rate_chart()
    charts['completion_rate'] = chart_to_png(completion_chart)

    # Clean up
    plt.close('all')

    return charts


def chart_to_png(fig: Figure) -> bytes:
    """Convert a matplotlib figure to PNG bytes.

    Args:
        fig: Matplotlib figure to convert

    Returns:
        bytes: PNG image data
    """
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    return buf.getvalue()


def get_procedure_status_chart() -> Figure:
    """Generate a pie chart showing distribution of procedure statuses.

    Returns:
        Figure: Matplotlib figure containing the chart
    """
    # Get status counts
    status_counts = (Procedure.objects.values('status')
                     .annotate(count=Count('id'))
                     .order_by('status'))

    # Extract data
    statuses = [s['status'] for s in status_counts]
    counts = [s['count'] for s in status_counts]

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(counts, labels=statuses, autopct='%1.1f%%')
    ax.set_title('Procedure Status Distribution')

    return fig


def get_procedure_timeline() -> Figure:
    """Generate a timeline chart showing procedures over time.

    Returns:
        Figure: Matplotlib figure containing the chart
    """
    # Get procedures ordered by start date
    procedures = (Procedure.objects.all()
                  .order_by('start_date')
                  .values('start_date', 'end_date', 'title'))

    # Extract data
    titles = [p['title'] for p in procedures]
    start_dates = [p['start_date'] for p in procedures]
    durations = [(p['end_date'] - p['start_date']).days for p in procedures]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(titles, durations, left=start_dates)
    ax.set_title('Procedure Timeline')

    return fig


def get_completion_rate_chart() -> Figure:
    """Generate a bar chart showing procedure completion rates.

    Returns:
        Figure: Matplotlib figure containing the chart
    """
    # Get completed vs total procedures by type
    procedures = (Procedure.objects.values('type')
                  .annotate(total=Count('id'),
                            completed=Count('id', filter=Q(status='completed')))
                  .order_by('type'))

    # Extract data
    types = [p['type'] for p in procedures]
    totals = [p['total'] for p in procedures]
    completed = [p['completed'] for p in procedures]
    completion_rates = [c / t * 100 for c, t in zip(completed, totals)]

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(types, completion_rates)
    ax.set_title('Procedure Completion Rates by Type')
    ax.set_ylabel('Completion Rate (%)')
    ax.set_ylim(0, 100)

    return fig
