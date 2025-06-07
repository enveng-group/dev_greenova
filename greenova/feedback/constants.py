"""constants.py.

Centralized constants and enumerations for the feedback app.

This module defines feedback types, statuses, and categories to improve
maintainability and reduce duplication across models, forms, and business logic.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Final

# Feedback types
FEEDBACK_TYPE_BUG: Final[str] = "bug"
FEEDBACK_TYPE_FEATURE: Final[str] = "feature"
FEEDBACK_TYPE_COMMENT: Final[str] = "comment"
FEEDBACK_TYPE_OTHER: Final[str] = "other"
FEEDBACK_TYPE_CHOICES: Final[list[tuple[str, str]]] = [
    (FEEDBACK_TYPE_BUG, "Bug Report"),
    (FEEDBACK_TYPE_FEATURE, "Feature Request"),
    (FEEDBACK_TYPE_COMMENT, "Comment"),
    (FEEDBACK_TYPE_OTHER, "Other"),
]

# Feedback statuses
FEEDBACK_STATUS_NEW: Final[str] = "new"
FEEDBACK_STATUS_IN_PROGRESS: Final[str] = "in_progress"
FEEDBACK_STATUS_RESOLVED: Final[str] = "resolved"
FEEDBACK_STATUS_CLOSED: Final[str] = "closed"
FEEDBACK_STATUS_CHOICES: Final[list[tuple[str, str]]] = [
    (FEEDBACK_STATUS_NEW, "New"),
    (FEEDBACK_STATUS_IN_PROGRESS, "In Progress"),
    (FEEDBACK_STATUS_RESOLVED, "Resolved"),
    (FEEDBACK_STATUS_CLOSED, "Closed"),
]

# Feedback categories (example)
FEEDBACK_CATEGORY_UI: Final[str] = "ui"
FEEDBACK_CATEGORY_PERFORMANCE: Final[str] = "performance"
FEEDBACK_CATEGORY_SECURITY: Final[str] = "security"
FEEDBACK_CATEGORY_OTHER: Final[str] = "other"
FEEDBACK_CATEGORY_CHOICES: Final[list[tuple[str, str]]] = [
    (FEEDBACK_CATEGORY_UI, "UI"),
    (FEEDBACK_CATEGORY_PERFORMANCE, "Performance"),
    (FEEDBACK_CATEGORY_SECURITY, "Security"),
    (FEEDBACK_CATEGORY_OTHER, "Other"),
]
