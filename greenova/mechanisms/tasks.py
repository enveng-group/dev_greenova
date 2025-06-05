"""Background and manual tasks for the mechanisms app.

All functions and classes are decorated with @beartype for runtime type checking.
"""
from beartype import beartype
import logging
from .models import EnvironmentalMechanism
from obligations.models import Obligation
from obligations.utils import is_obligation_overdue
from .types import MechanismDefinitionDict, MechanismStateDict, MechanismDefinitionManager, MechanismStateEvaluator

logger = logging.getLogger(__name__)

@beartype
def run_mechanism_checks() -> None:
    """Check for mechanisms with no obligations or with overdue obligations and log them."""
    mechanisms = EnvironmentalMechanism.objects.all()
    for mechanism in mechanisms:
        obligations = Obligation.objects.filter(primary_environmental_mechanism=mechanism)
        if not obligations.exists():
            logger.warning("Mechanism %s has no obligations assigned!", mechanism.name)
        else:
            overdue = [o for o in obligations if is_obligation_overdue(o)]
            if overdue:
                logger.warning(
                    "Mechanism %s has %d overdue obligations.",
                    mechanism.name,
                    len(overdue),
                )
    logger.info("Mechanism checks complete.")
