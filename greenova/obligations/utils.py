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


def is_obligation_overdue(
    obligation: Union['Obligation', Dict[str, Any]],
    reference_date: Optional[date] = None
) -> bool:
    """
    Determine if an obligation is overdue based on its status and due date.

    This is the canonical implementation for determining overdue status that should be
    used throughout the application to ensure consistency.

    Args:
        obligation: An Obligation model instance or dict with obligation attributes
        reference_date: Optional date to compare against (defaults to today)

    Returns:
        bool: True if the obligation is overdue, False otherwise
    """
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

    if status == STATUS_COMPLETED:
        return STATUS_COMPLETED

    if due_date and due_date < today:
        return STATUS_OVERDUE

    if due_date and today <= due_date <= today + timedelta(days=14):
        return STATUS_UPCOMING

    return status


def _match_frequency_pattern(frequency_lower: str) -> Optional[str]:
    """Helper function to match frequency patterns and return canonical form."""
    # Daily/Weekly patterns
    if any(term in frequency_lower for term in ['day', 'daily']):
        return FREQUENCY_DAILY
    if any(term in frequency_lower for term in ['fortnight', 'bi-week', 'biweek']):
        return FREQUENCY_FORTNIGHTLY
    if 'week' in frequency_lower:
        return FREQUENCY_WEEKLY

    # Monthly patterns
    monthly_patterns = {
        ('quarter', '3 month', 'three month'): FREQUENCY_QUARTERLY,
        ('biannual', 'bi annual', 'semi', 'twice a year'): FREQUENCY_BIANNUAL,
        ('annual', 'year', '12 month', 'twelve month'): FREQUENCY_ANNUAL
    }

    if 'month' in frequency_lower:
        for terms, freq in monthly_patterns.items():
            if any(term in frequency_lower for term in terms):
                return freq
        return FREQUENCY_MONTHLY

    return None


def normalize_frequency(frequency: str) -> str:
    """
    Normalize a frequency string to its canonical form.

    Args:
        frequency: A string representing the frequency

    Returns:
        str: The normalized frequency string
    """
    if not frequency:
        return ''

    frequency_lower = frequency.lower().strip()

    # Check if it's already in canonical form
    canonical_frequencies = {
        FREQUENCY_DAILY, FREQUENCY_WEEKLY, FREQUENCY_FORTNIGHTLY,
        FREQUENCY_MONTHLY, FREQUENCY_QUARTERLY, FREQUENCY_BIANNUAL,
        FREQUENCY_ANNUAL
    }
    if frequency_lower in canonical_frequencies:
        return frequency_lower

    # Check aliases first
    for alias, canonical in FREQUENCY_ALIASES.items():
        if alias in frequency_lower:
            return canonical

    # Try pattern matching
    matched_frequency = _match_frequency_pattern(frequency_lower)
    if matched_frequency:
        return matched_frequency

    return frequency_lower


def get_responsibility_display_name(responsibility_value: str) -> str:
    """Get the display name for a responsibility value."""
    if 'Perdaman' in responsibility_value or 'SCJV' in responsibility_value:
        return responsibility_value

    role_display = get_role_display(responsibility_value)
    if role_display != responsibility_value:
        return role_display

    return responsibility_value.replace('_', ' ').title()
