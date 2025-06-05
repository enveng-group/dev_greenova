"""Custom context processors for the obligations app.

Provides obligations status, counts, or compliance alerts for templates.

Returns:
    dict: Context variables for templates.
"""
from typing import Any, Dict
from beartype import beartype
from django.utils import timezone
from .models import Obligation

@beartype
def obligations_context(request) -> Dict[str, Any]:
    """Inject obligations-related context variables into templates.

    Args:
        request: The current HttpRequest object.

    Returns:
        A dictionary of obligations-related context variables, including:
            - active_obligations: Queryset of active obligations for the user.
            - compliance_status: Compliance status summary for the user.
            - next_due_obligation: The next due obligation for the user.
    """
    user = getattr(request, "user", None)
    active_obligations = Obligation.objects.none()
    compliance_status = "Unknown"
    next_due_obligation = None
    if user and user.is_authenticated:
        # Active obligations: assigned to user, not completed
        active_obligations = Obligation.objects.filter(
            assigned_to=user, status__in=["pending", "in_progress"]
        ).order_by("action_due_date")
        # Compliance status: simple example (customize as needed)
        overdue_count = active_obligations.filter(action_due_date__lt=timezone.now()).count()
        if overdue_count > 0:
            compliance_status = "Non-compliant"
        elif active_obligations.exists():
            compliance_status = "Compliant"
        else:
            compliance_status = "No active obligations"
        # Next due obligation
        next_due_obligation = active_obligations.filter(action_due_date__gte=timezone.now()).order_by("action_due_date").first()
    return {
        "active_obligations": active_obligations,
        "compliance_status": compliance_status,
        "next_due_obligation": next_due_obligation,
    }
