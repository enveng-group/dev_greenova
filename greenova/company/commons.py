"""commons.py.

Shared logic, helpers, and base classes for the company app.

This module centralizes reusable code to improve maintainability and reduce duplication.
"""

from beartype import beartype

COMPANY_ROLE_ADMIN = "admin"
COMPANY_ROLE_MEMBER = "member"
COMPANY_ROLE_VIEWER = "viewer"

COMPANY_ROLE_CHOICES = [
    (COMPANY_ROLE_ADMIN, "Admin"),
    (COMPANY_ROLE_MEMBER, "Member"),
    (COMPANY_ROLE_VIEWER, "Viewer"),
]


@beartype
def is_company_admin(user) -> bool:
    """Return True if the user is a company admin."""
    return (
        hasattr(user, "companymembership")
        and user.companymembership.role == COMPANY_ROLE_ADMIN
    )


# Add additional shared helpers or base classes here as needed.
