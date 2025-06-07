"""Background and manual tasks for the obligations app.

All functions and classes are decorated with @beartype for runtime type checking.
"""

import logging
from datetime import timedelta

from beartype import beartype
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Obligation
from .utils import is_obligation_overdue

logger = logging.getLogger(__name__)


@beartype
def send_obligation_reminders() -> None:
    """Send reminders for upcoming and overdue obligations to responsible users."""
    today = timezone.now().date()
    upcoming_window = today + timedelta(days=7)
    obligations = Obligation.objects.filter(
        action_due_date__isnull=False,
        status__in=["not started", "in progress"],
    )
    for obligation in obligations:
        due_date = obligation.action_due_date
        if not due_date:
            continue
        is_overdue = is_obligation_overdue(obligation)
        is_upcoming = today <= due_date <= upcoming_window
        if not (is_overdue or is_upcoming):
            continue
        # Get responsible users
        users = obligation.responsible_users.all()
        if not users:
            continue
        subject = (
            f"[Greenova] Obligation Reminder: {obligation.obligation_number} - "
            f"{'Overdue' if is_overdue else 'Upcoming'}"
        )
        message = (
            f"Obligation: {obligation.obligation}\n"
            f"Project: {obligation.project.name}\n"
            f"Due Date: {due_date}\n"
            f"Status: {obligation.status}\n"
            f"\nPlease review and take necessary action."
        )
        for user in users:
            if not user.email:
                continue
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                logger.info(
                    "Sent reminder to %s for obligation %s",
                    user.email,
                    obligation.obligation_number,
                )
            except Exception as e:
                logger.exception(
                    "Failed to send reminder to %s for obligation %s: %s",
                    user.email,
                    obligation.obligation_number,
                    str(e),
                )
