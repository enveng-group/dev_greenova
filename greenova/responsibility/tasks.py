"""Background and manual tasks for the responsibility app.

All functions and classes are decorated with @beartype for runtime type checking.
"""
from beartype import beartype
import logging
from obligations.models import Obligation
from .models import ResponsibilityAssignment

logger = logging.getLogger(__name__)

@beartype
def check_responsibility_compliance() -> None:
    """Check for obligations missing responsibility assignments and log them."""
    missing = Obligation.objects.filter(responsibility_assignments__isnull=True)
    count = missing.count()
    for obligation in missing:
        logger.warning(
            "Obligation %s (%s) has no responsibility assignments!",
            obligation.obligation_number,
            obligation.project.name if hasattr(obligation, 'project') else "N/A",
        )
    logger.info("Checked responsibility compliance: %d obligations missing assignments", count)
