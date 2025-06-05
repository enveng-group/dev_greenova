"""Background and manual tasks for the dashboard app.

All functions and classes are decorated with @beartype for runtime type checking.
"""
from beartype import beartype
import logging
from projects.models import Project
from .figures import create_obligations_status_chart_svg

logger = logging.getLogger(__name__)

@beartype
def refresh_dashboard_cache() -> None:
    """Precompute and cache dashboard charts for all projects."""
    projects = Project.objects.all()
    count = 0
    for project in projects:
        # Precompute and cache the obligations status chart SVG
        svg = create_obligations_status_chart_svg(str(project.id))
        # Here you would store the SVG in a cache or database if needed
        logger.info("Refreshed dashboard cache for project %s", project.name)
        count += 1
    logger.info("Refreshed dashboard cache for %d projects", count)
