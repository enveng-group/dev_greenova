"""Dashboard chart generation using Matplotlib with SVG output and Plotly.js integration.

This module provides SVG pie chart generation for the dashboard, following the
requirements of Issue #165 for obligation drilldown functionality.
"""

import io
import logging
from typing import Any

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from beartype import beartype
from django.db.models import QuerySet
from django.utils import timezone
from matplotlib.figure import Figure
from mechanisms.models import EnvironmentalMechanism
from obligations.models import Obligation
from procedures.models import Procedure
from projects.models import Project

logger = logging.getLogger(__name__)

# Color scheme for status indicators (matching PicoCSS theme)
STATUS_COLORS = {
    "Not Started": "#f9c74f",  # Yellow
    "In Progress": "#90be6d",  # Green
    "Completed": "#43aa8b",    # Teal
    "Overdue": "#f94144",      # Red
}


@beartype
def create_obligations_status_chart_svg(project_id: str | None) -> str:
    """Create SVG pie chart for obligations status in a specific project.

    Args:
        project_id: Project ID to filter obligations by, or None for all projects

    Returns:
        SVG string representing the pie chart

    """
    try:
        if not project_id or project_id == "0":
            return '<svg><text x="50%" y="50%" text-anchor="middle">No project selected</text></svg>'

        # Get obligations for the project
        obligations = Obligation.objects.filter(project_id=project_id)

        if not obligations.exists():
            return '<svg><text x="50%" y="50%" text-anchor="middle">No obligations found</text></svg>'

        # Calculate status counts including overdue
        status_counts = _calculate_obligation_status_counts(obligations)

        # Create matplotlib figure for SVG generation
        fig = _create_pie_chart_figure(status_counts, "Project Obligations Status")

        # Convert to SVG
        svg_string = _figure_to_svg(fig)
        plt.close(fig)

        return svg_string

    except Exception as e:
        logger.exception("Error creating obligations status chart: %s", e)
        return f'<svg><text x="50%" y="50%" text-anchor="middle">Error: {e}</text></svg>'


@beartype
def create_project_compliance_chart(
        projects: QuerySet[Project]) -> tuple[go.Figure, bytes]:
    """Create project compliance chart for dashboard overview.

    Args:
        projects: QuerySet of projects to include in chart

    Returns:
        Tuple of (Plotly figure, PNG bytes for fallback)

    """
    try:
        if not projects.exists():
            # Return empty chart
            fig = go.Figure()
            fig.add_annotation(
                text="No projects available",
                x=0.5, y=0.5,
                xref="paper", yref="paper",
                showarrow=False,
            )
            return fig, b""

        # Calculate compliance data for each project
        project_data = []
        for project in projects:
            obligations = project.obligations.all()
            if obligations.exists():
                total = obligations.count()
                completed = obligations.filter(status="completed").count()
                compliance_rate = (completed / total) * 100 if total > 0 else 0

                project_data.append({
                    "name": project.name,
                    "compliance_rate": compliance_rate,
                    "total_obligations": total,
                    "completed_obligations": completed,
                })

        if not project_data:
            fig = go.Figure()
            fig.add_annotation(
                text="No obligation data available",
                x=0.5, y=0.5,
                xref="paper", yref="paper",
                showarrow=False,
            )
            return fig, b""

        # Create Plotly bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=[p["name"] for p in project_data],
                y=[p["compliance_rate"] for p in project_data],
                marker_color=[
                    "#43aa8b" if rate >= 80 else "#f9c74f" if rate >= 60 else "#f94144"
                    for rate in [p["compliance_rate"] for p in project_data]
                ],
                text=[f"{rate:.1f}%" for rate in [p["compliance_rate"] for p in project_data]],
                textposition="auto",
            ),
        ])

        fig.update_layout(
            title="Project Compliance Rates",
            xaxis_title="Projects",
            yaxis_title="Compliance Rate (%)",
            yaxis={"range": [0, 100]},
        )

        # Create fallback PNG
        png_bytes = fig.to_image(format="png")

        return fig, png_bytes

    except Exception as e:
        logger.exception("Error creating project compliance chart: %s", e)
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error: {e}",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
        )
        return fig, b""


@beartype
def create_mechanism_pie_chart_svg(project_id: str) -> str:
    """Create SVG pie chart showing mechanism distribution for a project.

    Args:
        project_id: Project ID to get mechanisms for

    Returns:
        SVG string representing the pie chart

    """
    try:
        from mechanisms.models import EnvironmentalMechanism

        mechanisms = EnvironmentalMechanism.objects.filter(project_id=project_id)

        if not mechanisms.exists():
            return '<svg><text x="50%" y="50%" text-anchor="middle">No mechanisms found</text></svg>'

        # Calculate mechanism data
        mechanism_data = {}
        for mechanism in mechanisms:
            total_obligations = mechanism.total_obligations
            if total_obligations > 0:
                mechanism_data[mechanism.name] = total_obligations

        if not mechanism_data:
            return '<svg><text x="50%" y="50%" text-anchor="middle">No obligations in mechanisms</text></svg>'

        # Create pie chart
        fig = _create_mechanism_pie_chart_figure(mechanism_data)
        svg_string = _figure_to_svg(fig)
        plt.close(fig)

        return svg_string

    except Exception as e:
        logger.exception("Error creating mechanism pie chart: %s", e)
        return f'<svg><text x="50%" y="50%" text-anchor="middle">Error: {e}</text></svg>'


@beartype
def create_procedure_pie_chart_svg(mechanism_id: str) -> str:
    """Create SVG pie chart showing procedure distribution for a mechanism.

    Args:
        mechanism_id: Mechanism ID to get procedures for

    Returns:
        SVG string representing the pie chart

    """
    try:
        obligations = Obligation.objects.filter(
            primary_environmental_mechanism_id=mechanism_id,
        )

        if not obligations.exists():
            return '<svg><text x="50%" y="50%" text-anchor="middle">No obligations found</text></svg>'

        # Count obligations by procedure
        procedure_counts = {}
        for obligation in obligations:
            procedure = obligation.procedure or "Unknown"
            procedure_counts[procedure] = procedure_counts.get(procedure, 0) + 1

        if not procedure_counts:
            return '<svg><text x="50%" y="50%" text-anchor="middle">No procedures found</text></svg>'

        # Create pie chart
        fig = _create_procedure_pie_chart_figure(procedure_counts)
        svg_string = _figure_to_svg(fig)
        plt.close(fig)

        return svg_string

    except Exception as e:
        logger.exception("Error creating procedure pie chart: %s", e)
        return f'<svg><text x="50%" y="50%" text-anchor="middle">Error: {e}</text></svg>'


@beartype
def create_mechanism_pie_chart_svg(mechanism_id: int) -> str:
    """Create SVG pie chart for a specific mechanism's obligation status.

    Args:
        mechanism_id: ID of the mechanism to create chart for

    Returns:
        SVG string representing the pie chart

    """
    try:
        mechanism = EnvironmentalMechanism.objects.get(id=mechanism_id)

        # Get status counts from the mechanism
        status_counts = {
            "Not Started": mechanism.not_started_count,
            "In Progress": mechanism.in_progress_count,
            "Completed": mechanism.completed_count,
            "Overdue": mechanism.overdue_count,
        }

        # Filter out zero values
        filtered_counts = {k: v for k, v in status_counts.items() if v > 0}

        if not filtered_counts:
            return '<svg><text x="50%" y="50%" text-anchor="middle">No obligations found</text></svg>'

        # Create matplotlib figure for SVG generation
        fig = _create_pie_chart_figure(filtered_counts, f"Mechanism: {mechanism.name}")

        # Convert to SVG
        svg_string = _figure_to_svg(fig)
        plt.close(fig)

        return svg_string

    except EnvironmentalMechanism.DoesNotExist:
        logger.exception("Mechanism with ID %s does not exist", mechanism_id)
        return '<svg><text x="50%" y="50%" text-anchor="middle">Mechanism not found</text></svg>'
    except Exception as e:
        logger.exception("Error creating mechanism pie chart: %s", e)
        return f'<svg><text x="50%" y="50%" text-anchor="middle">Error: {e}</text></svg>'


@beartype
def create_procedure_pie_chart_svg(
        procedure_id: int, chart_data: dict[str, int]) -> str:
    """Create SVG pie chart for a specific procedure's obligation status.

    Args:
        procedure_id: ID of the procedure to create chart for
        chart_data: Dictionary with status counts

    Returns:
        SVG string representing the pie chart

    """
    try:
        procedure = Procedure.objects.get(id=procedure_id)

        # Filter out zero values
        filtered_counts = {k: v for k, v in chart_data.items() if v > 0}

        if not filtered_counts:
            return '<svg><text x="50%" y="50%" text-anchor="middle">No obligations found</text></svg>'

        # Create matplotlib figure for SVG generation
        fig = _create_pie_chart_figure(filtered_counts, f"Procedure: {procedure.name}")

        # Convert to SVG
        svg_string = _figure_to_svg(fig)
        plt.close(fig)

        return svg_string

    except Procedure.DoesNotExist:
        logger.exception("Procedure with ID %s does not exist", procedure_id)
        return '<svg><text x="50%" y="50%" text-anchor="middle">Procedure not found</text></svg>'
    except Exception as e:
        logger.exception("Error creating procedure pie chart: %s", e)
        return f'<svg><text x="50%" y="50%" text-anchor="middle">Error: {e}</text></svg>'


@beartype
def _calculate_obligation_status_counts(
        obligations: QuerySet[Obligation]) -> dict[str, int]:
    """Calculate status counts for obligations, including overdue detection."""
    counts = {
        "Not Started": 0,
        "In Progress": 0,
        "Completed": 0,
        "Overdue": 0,
    }

    today = timezone.now().date()

    for obligation in obligations:
        # Check if overdue (due date passed and not completed)
        if (obligation.action_due_date and
            obligation.action_due_date < today and
                obligation.status != "completed"):
            counts["Overdue"] += 1
        else:
            # Regular status counting
            status = obligation.status
            if status == "not started":
                counts["Not Started"] += 1
            elif status == "in progress":
                counts["In Progress"] += 1
            elif status == "completed":
                counts["Completed"] += 1

    return counts


@beartype
def _create_pie_chart_figure(data: dict[str, int], title: str) -> Figure:
    """Create a matplotlib figure with a pie chart with enhanced interactivity."""
    fig, ax = plt.subplots(figsize=(6, 6))

    # Filter out zero values
    filtered_data = {k: v for k, v in data.items() if v > 0}

    if not filtered_data:
        ax.text(0.5, 0.5, "No data available",
                horizontalalignment="center", verticalalignment="center",
                transform=ax.transAxes, fontsize=12)
        ax.set_title(title)
        return fig

    labels = list(filtered_data.keys())
    values = list(filtered_data.values())
    colors = [STATUS_COLORS.get(label, "#cccccc") for label in labels]

    # Create pie chart
    wedges, _texts, autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1},
    )

    # Add click data attributes to wedges for JavaScript interaction
    for i, (wedge, label, value) in enumerate(
            zip(wedges, labels, values, strict=False)):
        # Set GID for JavaScript targeting
        wedge.set_gid(f"status_{label.lower().replace(' ', '_')}_{i}")
        # Add custom properties for data attributes
        wedge.set_label(label)  # Store original label
        wedge.status_value = value  # Store value for JavaScript access

    # Styling
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_weight("bold")
        autotext.set_fontsize(10)

    ax.set_title(title, fontsize=14, fontweight="bold", pad=20)
    ax.axis("equal")

    return fig


@beartype
def _create_mechanism_pie_chart_figure(mechanism_data: dict[str, int]) -> Figure:
    """Create pie chart figure for mechanism distribution."""
    fig, ax = plt.subplots(figsize=(8, 8))

    labels = list(mechanism_data.keys())
    values = list(mechanism_data.values())

    # Use a color palette for mechanisms
    colors = plt.cm.Set3(range(len(labels)))

    wedges, _texts, _autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )

    # Add click data attributes to wedges for JavaScript interaction
    for i, wedge in enumerate(wedges):
        wedge.set_gid(f"mechanism_{i}")  # Add ID for JavaScript targeting

    ax.set_title(
        "Mechanisms by Obligation Count",
        fontsize=16,
        fontweight="bold",
        pad=20)
    ax.axis("equal")

    return fig


@beartype
def _create_procedure_pie_chart_figure(procedure_data: dict[str, int]) -> Figure:
    """Create pie chart figure for procedure distribution."""
    fig, ax = plt.subplots(figsize=(8, 8))

    labels = list(procedure_data.keys())
    values = list(procedure_data.values())

    # Use a different color palette for procedures
    colors = plt.cm.Pastel1(range(len(labels)))

    wedges, _texts, _autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )

    # Add click data attributes to wedges for JavaScript interaction
    for i, wedge in enumerate(wedges):
        wedge.set_gid(f"procedure_{i}")  # Add ID for JavaScript targeting

    ax.set_title(
        "Procedures by Obligation Count",
        fontsize=16,
        fontweight="bold",
        pad=20)
    ax.axis("equal")

    return fig


@beartype
def _figure_to_svg(fig: Figure) -> str:
    """Convert matplotlib figure to SVG string with enhanced interactive elements.

    This function converts matplotlib figures to SVG and adds CSS classes and
    data attributes to enable JavaScript interactivity for the drilldown system.
    """
    import re

    svg_buffer = io.StringIO()
    fig.savefig(svg_buffer, format="svg", bbox_inches="tight",
                facecolor="white", edgecolor="none")
    svg_buffer.seek(0)
    svg_string = svg_buffer.getvalue()
    svg_buffer.close()

    # Add interactive chart class to the main SVG element
    svg_string = svg_string.replace(
        "<svg", '<svg class="interactive-chart dashboard-chart"')

    # Add CSS classes and data attributes to pie chart paths for interactivity
    # This regex matches SVG path elements that are likely pie wedges
    path_pattern = r'(<path[^>]*d="[^"]*L[^"]*A[^"]*Z"[^>]*>)'
    paths = re.findall(path_pattern, svg_string)

    for i, path in enumerate(paths):
        # Add CSS classes and data attributes for JavaScript targeting
        enhanced_path = path.replace(
            "<path",
            f'<path class="chart-wedge pie-segment" '
            f'data-segment-index="{i}" '
            f'data-chart-type="pie" '
            f'tabindex="0" '
            f'role="button" '
            f'aria-label="Chart segment {i + 1}" ',
        )
        svg_string = svg_string.replace(path, enhanced_path)

    # Add CSS classes to text elements for better styling
    svg_string = re.sub(r"(<text[^>]*>)", r'<text class="chart-text">\1</text>'.replace(
        '<text class="chart-text"><text', '<text class="chart-text"'), svg_string, )

    # Fix the text replacement to avoid double tags
    svg_string = re.sub(
        r'<text class="chart-text">(<text[^>]*>)',
        r'<text class="chart-text" \1',
        svg_string,
    )

    # Add a container group for better organization
    svg_string = re.sub(
        r'(<g id="figure_1">)',
        r'<g id="chart-container" class="chart-container">\1',
        svg_string,
    )

    # Close the container group
    svg_string = re.sub(
        r"(</g>\s*</svg>)$",
        r"</g>\1",
        svg_string,
    )

    # Add ARIA attributes for accessibility
    return svg_string.replace(
        'class="interactive-chart dashboard-chart"',
        'class="interactive-chart dashboard-chart" '
        'role="img" '
        'aria-label="Interactive dashboard chart" '
        'tabindex="0"',
    )


@beartype
def get_plotly_chart_data(project_id: str | None) -> dict[str, Any]:
    """Get chart data in Plotly.js compatible format for client-side rendering.

    This function bridges matplotlib SVG generation with Plotly.js interactivity
    as required by the issue specifications.

    Args:
        project_id: Project ID to get data for

    Returns:
        Dictionary containing Plotly.js compatible data and layout

    """
    try:
        if not project_id or project_id == "0":
            return {
                "data": [],
                "layout": {
                    "title": "No project selected",
                    "annotations": [{
                        "text": "Please select a project",
                        "x": 0.5,
                        "y": 0.5,
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                    }],
                },
            }

        obligations = Obligation.objects.filter(project_id=project_id)
        status_counts = _calculate_obligation_status_counts(obligations)

        # Filter out zero values
        filtered_counts = {k: v for k, v in status_counts.items() if v > 0}

        if not filtered_counts:
            return {
                "data": [],
                "layout": {
                    "title": "No obligations found",
                    "annotations": [{
                        "text": "No obligations in this project",
                        "x": 0.5,
                        "y": 0.5,
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                    }],
                },
            }

        # Create Plotly.js data
        return {
            "data": [{
                "values": list(filtered_counts.values()),
                "labels": list(filtered_counts.keys()),
                "type": "pie",
                "marker": {
                    "colors": [STATUS_COLORS.get(label, "#cccccc")
                               for label in filtered_counts],
                },
                "textinfo": "label+percent",
                "textposition": "auto",
                "hovertemplate": "<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
            }],
            "layout": {
                "title": {
                    "text": "Project Obligations Status",
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

    except Exception as e:
        logger.exception("Error creating Plotly chart data: %s", e)
        return {
            "data": [],
            "layout": {
                "title": f"Error: {e}",
                "annotations": [{
                    "text": f"Error loading chart: {e}",
                    "x": 0.5,
                    "y": 0.5,
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                }],
            },
        }
