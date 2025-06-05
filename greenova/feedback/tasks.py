"""Background and manual tasks for the feedback app.

All functions and classes are decorated with @beartype for runtime type checking.
"""
from beartype import beartype
import logging
from .models import BugReport

logger = logging.getLogger(__name__)

@beartype
def process_feedback_queue() -> None:
    """Process and mark as handled any unprocessed bug reports."""
    unprocessed = BugReport.objects.filter(status__in=["new", "open"])
    count = 0
    for report in unprocessed:
        # Here you would implement actual triage/notification logic
        report.status = "handled"
        report.save()
        logger.info("Processed feedback report %s: marked as handled", report.id)
        count += 1
    logger.info("Processed %d feedback reports from the queue", count)
