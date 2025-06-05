"""Custom context processors for the dashboard app.

Provides dashboard notifications, stats, or quick links for templates.

Returns:
    dict: Context variables for templates.
"""
from typing import Any, Dict
from beartype import beartype
from django.contrib.auth import get_user_model
from obligations.models import Obligation
from django.utils import timezone

@beartype
def dashboard_context(request) -> Dict[str, Any]:
    """Inject dashboard-related context variables into templates.

    Args:
        request: The current HttpRequest object.

    Returns:
        A dictionary of dashboard-related context variables, including:
            - unread_notifications: Count of unread notifications for the user.
            - pending_tasks: Count of pending obligations for the user.
            - dashboard_alerts: List of dashboard alert messages.
    """
    user = getattr(request, "user", None)
    unread_notifications = 0
    pending_tasks = 0
    dashboard_alerts = []
    if user and user.is_authenticated:
        # Example: Unread notifications (stub, replace with real logic if available)
        if hasattr(user, "notifications"):
            unread_notifications = user.notifications.filter(read=False).count()
        # Pending obligations assigned to user
        pending_tasks = Obligation.objects.filter(
            assigned_to=user, status="pending"
        ).count()
        # Example: Add alert if user has overdue obligations
        overdue_count = Obligation.objects.filter(
            assigned_to=user, due_date__lt=timezone.now(), status="pending"
        ).count()
        if overdue_count > 0:
            dashboard_alerts.append(
                f"You have {overdue_count} overdue obligations. Please review them."
            )
    return {
        "unread_notifications": unread_notifications,
        "pending_tasks": pending_tasks,
        "dashboard_alerts": dashboard_alerts,
    }
