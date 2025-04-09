import logging
from datetime import date, timedelta
from typing import Any, Dict, Optional, Union

from core.utils.roles import get_role_display
from django.utils import timezone

from .constants import (FREQUENCY_ALIASES, FREQUENCY_ANNUAL, FREQUENCY_BIANNUAL,
                        FREQUENCY_DAILY, FREQUENCY_FORTNIGHTLY, FREQUENCY_MONTHLY,
                        FREQUENCY_QUARTERLY, FREQUENCY_WEEKLY, STATUS_COMPLETED,
                        STATUS_OVERDUE, STATUS_UPCOMING)

logger = logging.getLogger(__name__)

def is_obligation_overdue(obligation: Union['Obligation', Dict[str, Any]], reference_date: Optional[date] = None) -> bool:
    """
    Determine if an obligation is overdue based on its status and due date.

    This is the canonical implementation for determining overdue status that should
    be used throughout the application to ensure consistency.

    Args:
        obligation: An Obligation model instance or a dictionary with obligation attributes
        reference_date: Optional date to compare against (defaults to today)

    Returns:
        bool: True if the obligation is overdue, False otherwise
    """
    # Use today as reference date if none provided
    if reference_date is None:
        reference_date = timezone.now().date()

    # Get status - handle both model instances and dictionaries
    if isinstance(obligation, dict):
        status = obligation.get('status')
        due_date = obligation.get('action_due_date')
    else:
        status = obligation.status
        due_date = obligation.action_due_date

    # Rule 1: Completed obligations are never overdue
    if status == STATUS_COMPLETED:
        return False

    # Rule 2: Obligations without a due date cannot be overdue
    if not due_date:
        return False

    # Rule 3: If the due date is in the past and not completed, it's overdue
    return due_date < reference_date

def get_obligation_status(obligation):
    """
    Determine the real status of an obligation based on its due date and current status.

    Returns one of: 'overdue', 'upcoming', 'completed', or the original status.
    """
    status = getattr(obligation, 'status', '').lower()
    due_date = getattr(obligation, 'action_due_date', None)
    today = timezone.now().date()

    # Completed obligations keep their status
    if status == STATUS_COMPLETED:
        return STATUS_COMPLETED

    # Check for overdue obligations
    if due_date and due_date < today:
        return STATUS_OVERDUE

    # Check for upcoming obligations (due within 14 days)
    if due_date and today <= due_date <= today + timedelta(days=14):
        return STATUS_UPCOMING

    # Return original status if not overdue or upcoming
    return status

def normalize_frequency(frequency: str) -> str:
    """
    Normalize a frequency string to its canonical form.

    This handles variations in terminology and ensures consistency
    across the application.

    Args:
        frequency: A string representing the frequency

    Returns:
        str: The normalized frequency string
    """
    if not frequency:
        return ''

    # Convert to lowercase for case-insensitive matching
    frequency_lower = frequency.lower().strip()

    # Check if it's one of our canonical values
    if frequency_lower in [
        FREQUENCY_DAILY, FREQUENCY_WEEKLY, FREQUENCY_FORTNIGHTLY,
        FREQUENCY_MONTHLY, FREQUENCY_QUARTERLY, FREQUENCY_BIANNUAL, FREQUENCY_ANNUAL
    ]:
        return frequency_lower

    # Check aliases
    for alias, canonical in FREQUENCY_ALIASES.items():
        if alias in frequency_lower:
            return canonical

    # Handle common variations
    if 'day' in frequency_lower or 'daily' in frequency_lower:
        return FREQUENCY_DAILY
    elif 'week' in frequency_lower:
        return FREQUENCY_WEEKLY
    elif 'fortnight' in frequency_lower or 'bi-week' in frequency_lower or 'biweek' in frequency_lower:
        return FREQUENCY_FORTNIGHTLY
    elif 'month' in frequency_lower:
        return FREQUENCY_MONTHLY
    elif 'quarter' in frequency_lower or '3 month' in frequency_lower or 'three month' in frequency_lower:
        return FREQUENCY_QUARTERLY
    elif 'biannual' in frequency_lower or 'bi annual' in frequency_lower or 'semi' in frequency_lower or 'twice a year' in frequency_lower or '6 month' in frequency_lower:
        return FREQUENCY_BIANNUAL
    elif 'annual' in frequency_lower or 'year' in frequency_lower or '12 month' in frequency_lower or 'twelve month' in frequency_lower:
        return FREQUENCY_ANNUAL

    # If we can't normalize it, return as-is
    return frequency_lower

def get_responsibility_display_name(responsibility_value: str) -> str:
    """
    Get the display name for a responsibility value.

    Args:
        responsibility_value: The responsibility value to get display name for

    Returns:
        str: The display name for the responsibility
    """
    # First check if this is already a display name (as stored in older records)
    if 'Perdaman' in responsibility_value or 'SCJV' in responsibility_value:
        return responsibility_value

    # Try to get role display from the role utilities
    role_display = get_role_display(responsibility_value)
    if role_display != responsibility_value:  # If we got a match
        return role_display

    # Fallback: just return the input with title casing for readability
    return responsibility_value.replace('_', ' ').title()
