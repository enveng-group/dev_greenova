"""constants.py.

Centralized constants and enumerations for the dashboard app.

This module defines widget types, status indicators, and display options to improve
maintainability and reduce duplication across models, views, and templates.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Final

# Dashboard widget types
WIDGET_TYPE_CHART: Final[str] = "chart"
WIDGET_TYPE_TABLE: Final[str] = "table"
WIDGET_TYPE_METRIC: Final[str] = "metric"
WIDGET_TYPE_ALERT: Final[str] = "alert"
WIDGET_TYPE_CHOICES: Final[list[tuple[str, str]]] = [
    (WIDGET_TYPE_CHART, "Chart"),
    (WIDGET_TYPE_TABLE, "Table"),
    (WIDGET_TYPE_METRIC, "Metric"),
    (WIDGET_TYPE_ALERT, "Alert"),
]

# Status indicators
STATUS_OK: Final[str] = "ok"
STATUS_WARNING: Final[str] = "warning"
STATUS_ERROR: Final[str] = "error"
STATUS_UNKNOWN: Final[str] = "unknown"
STATUS_INDICATOR_CHOICES: Final[list[tuple[str, str]]] = [
    (STATUS_OK, "OK"),
    (STATUS_WARNING, "Warning"),
    (STATUS_ERROR, "Error"),
    (STATUS_UNKNOWN, "Unknown"),
]

# Display options
DISPLAY_OPTION_COMPACT: Final[str] = "compact"
DISPLAY_OPTION_EXPANDED: Final[str] = "expanded"
DISPLAY_OPTION_CHOICES: Final[list[tuple[str, str]]] = [
    (DISPLAY_OPTION_COMPACT, "Compact"),
    (DISPLAY_OPTION_EXPANDED, "Expanded"),
]
