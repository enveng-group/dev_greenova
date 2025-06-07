"""Background and manual tasks for the auditing app.

All functions and classes are decorated with @beartype for runtime type checking.
"""

import logging
from datetime import timedelta

from beartype import beartype
from django.utils import timezone

from .models import AuditEntry

logger = logging.getLogger(__name__)


@beartype
def cleanup_audit_logs() -> None:
    """Delete audit entries older than 2 years to maintain audit log size."""
    cutoff_date = timezone.now() - timedelta(days=730)
    old_entries = AuditEntry.objects.filter(created_at__lt=cutoff_date)
    count = old_entries.count()
    old_entries.delete()
    logger.info("Deleted %d audit entries older than 2 years", count)
