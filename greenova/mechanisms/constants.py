"""constants.py.

Centralized constants and enumerations for the mechanisms app.

This module defines mechanism types, categories, and operational modes to improve
maintainability and reduce duplication across models, forms, and business logic.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Final

# Mechanism types
MECHANISM_TYPE_PHYSICAL: Final[str] = "physical"
MECHANISM_TYPE_CHEMICAL: Final[str] = "chemical"
MECHANISM_TYPE_BIOLOGICAL: Final[str] = "biological"
MECHANISM_TYPE_OTHER: Final[str] = "other"
MECHANISM_TYPE_CHOICES: Final[list[tuple[str, str]]] = [
    (MECHANISM_TYPE_PHYSICAL, "Physical"),
    (MECHANISM_TYPE_CHEMICAL, "Chemical"),
    (MECHANISM_TYPE_BIOLOGICAL, "Biological"),
    (MECHANISM_TYPE_OTHER, "Other"),
]

# Mechanism categories
MECHANISM_CATEGORY_PREVENTION: Final[str] = "prevention"
MECHANISM_CATEGORY_CONTROL: Final[str] = "control"
MECHANISM_CATEGORY_MITIGATION: Final[str] = "mitigation"
MECHANISM_CATEGORY_CHOICES: Final[list[tuple[str, str]]] = [
    (MECHANISM_CATEGORY_PREVENTION, "Prevention"),
    (MECHANISM_CATEGORY_CONTROL, "Control"),
    (MECHANISM_CATEGORY_MITIGATION, "Mitigation"),
]

# Operational modes
OPERATIONAL_MODE_AUTOMATIC: Final[str] = "automatic"
OPERATIONAL_MODE_MANUAL: Final[str] = "manual"
OPERATIONAL_MODE_CHOICES: Final[list[tuple[str, str]]] = [
    (OPERATIONAL_MODE_AUTOMATIC, "Automatic"),
    (OPERATIONAL_MODE_MANUAL, "Manual"),
]
