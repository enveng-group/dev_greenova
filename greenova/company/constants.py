"""constants.py.

Centralized constants and enumerations for the company app.

This module defines company types, statuses, and roles to improve
maintainability and reduce duplication across models, forms, and business logic.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Final

# Company types
COMPANY_TYPE_PRIVATE: Final[str] = "private"
COMPANY_TYPE_PUBLIC: Final[str] = "public"
COMPANY_TYPE_GOVERNMENT: Final[str] = "government"
COMPANY_TYPE_NONPROFIT: Final[str] = "nonprofit"
COMPANY_TYPE_CHOICES: Final[list[tuple[str, str]]] = [
    (COMPANY_TYPE_PRIVATE, "Private"),
    (COMPANY_TYPE_PUBLIC, "Public"),
    (COMPANY_TYPE_GOVERNMENT, "Government"),
    (COMPANY_TYPE_NONPROFIT, "Nonprofit"),
]

# Company statuses
COMPANY_STATUS_ACTIVE: Final[str] = "active"
COMPANY_STATUS_INACTIVE: Final[str] = "inactive"
COMPANY_STATUS_PENDING: Final[str] = "pending"
COMPANY_STATUS_CHOICES: Final[list[tuple[str, str]]] = [
    (COMPANY_STATUS_ACTIVE, "Active"),
    (COMPANY_STATUS_INACTIVE, "Inactive"),
    (COMPANY_STATUS_PENDING, "Pending"),
]

# Company roles
COMPANY_ROLE_OWNER: Final[str] = "owner"
COMPANY_ROLE_MANAGER: Final[str] = "manager"
COMPANY_ROLE_EMPLOYEE: Final[str] = "employee"
COMPANY_ROLE_CHOICES: Final[list[tuple[str, str]]] = [
    (COMPANY_ROLE_OWNER, "Owner"),
    (COMPANY_ROLE_MANAGER, "Manager"),
    (COMPANY_ROLE_EMPLOYEE, "Employee"),
]
