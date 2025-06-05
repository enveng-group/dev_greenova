"""Background and manual tasks for the reports app.

All functions and classes are decorated with @beartype for runtime type checking.
"""
from beartype import beartype
import logging
from datetime import timedelta
from django.utils import timezone
from .models import Report
from .types import ReportPayloadDict, ExportFormatDict, ReportResultDict, ReportPayloadManager, ExportFormatter, ResultProcessor

logger = logging.getLogger(__name__)

@beartype
def generate_scheduled_reports() -> None:
    """Generate a summary report for all reports created in the last 7 days and log the action."""
    one_week_ago = timezone.now() - timedelta(days=7)
    recent_reports = Report.objects.filter(created_at__gte=one_week_ago)
    count = recent_reports.count()
    if count == 0:
        logger.info("No new reports to summarize in the last 7 days.")
        return
    summary = f"Summary: {count} reports created in the last 7 days."
    logger.info(summary)
    # Optionally, create a new Report entry as a summary (example only)
    Report.objects.create(
        name="Weekly Report Summary",
        description=summary,
    )
    logger.info("Created weekly summary report.")
