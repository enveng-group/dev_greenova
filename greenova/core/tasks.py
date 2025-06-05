"""Background and manual tasks for the core app.

All functions and classes are decorated with @beartype for runtime type checking.
"""
from beartype import beartype
import logging
from django.db import connections
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)

@beartype
def system_health_check() -> None:
    """Perform a system health check and log results."""
    db_conn = connections['default']
    try:
        db_conn.cursor()
        logger.info("System health check: Database connection OK.")
    except OperationalError as e:
        logger.error("System health check: Database connection FAILED: %s", str(e))
        # Optionally, send an alert or notification here
