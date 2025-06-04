"""constants.py.

Centralized constants and enumerations for the auditing app.

This module defines status choices and other shared constants to improve
maintainability and reduce duplication across models, forms, and business logic.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Final

# Mitigation status choices
MITIGATION_STATUS_OPEN: Final[str] = "open"
MITIGATION_STATUS_CLOSED: Final[str] = "closed"
MITIGATION_STATUS_ACTION_REQUIRED: Final[str] = "action_required"
MITIGATION_STATUS_CHOICES: Final[list[tuple[str, str]]] = [
    (MITIGATION_STATUS_OPEN, "Open"),
    (MITIGATION_STATUS_CLOSED, "Closed"),
    (MITIGATION_STATUS_ACTION_REQUIRED, "Action Required"),
]

# CorrectiveAction status choices
CORRECTIVE_ACTION_STATUS_OPEN: Final[str] = "open"
CORRECTIVE_ACTION_STATUS_IN_PROGRESS: Final[str] = "in_progress"
CORRECTIVE_ACTION_STATUS_CLOSED: Final[str] = "closed"
CORRECTIVE_ACTION_STATUS_OVERDUE: Final[str] = "overdue"
CORRECTIVE_ACTION_STATUS_CHOICES: Final[list[tuple[str, str]]] = [
    (CORRECTIVE_ACTION_STATUS_OPEN, "Open"),
    (CORRECTIVE_ACTION_STATUS_IN_PROGRESS, "In Progress"),
    (CORRECTIVE_ACTION_STATUS_CLOSED, "Closed"),
    (CORRECTIVE_ACTION_STATUS_OVERDUE, "Overdue"),
]
