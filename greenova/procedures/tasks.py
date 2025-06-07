"""Background and manual tasks for the procedures app.

All functions and classes are decorated with @beartype for runtime type checking.
"""

import logging

from beartype import beartype
from django.utils import timezone

from .models import Procedure

logger = logging.getLogger(__name__)


@beartype
def review_procedures() -> None:
    """Review procedures due for review and update their status/log actions.

    Finds all active procedures whose review_date is today or earlier and status is not 'review'.
    Updates their status to 'review' and logs the action.
    """
    today = timezone.now().date()
    due_procedures = Procedure.objects.filter(
        is_active=True,
        review_date__isnull=False,
        review_date__lte=today,
    ).exclude(status="review")
    count = 0
    for procedure in due_procedures:
        old_status = procedure.status
        procedure.set_status("review")
        logger.info(
            "Procedure %s (%s) marked as due for review (was %s)",
            procedure.name,
            procedure.document_id,
            old_status,
        )
        count += 1
    logger.info("Reviewed %d procedures due for review.", count)
