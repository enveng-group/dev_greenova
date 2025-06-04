"""constants.py.

Centralized constants and enumerations for the authentication app.

This module defines status choices, token types, and other shared constants to improve
maintainability and reduce duplication across models, forms, and business logic.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Final

# User roles
ROLE_USER: Final[str] = "user"
ROLE_STAFF: Final[str] = "staff"
ROLE_ADMIN: Final[str] = "admin"
ROLE_SUPERUSER: Final[str] = "superuser"
USER_ROLE_CHOICES: Final[list[tuple[str, str]]] = [
    (ROLE_USER, "User"),
    (ROLE_STAFF, "Staff"),
    (ROLE_ADMIN, "Admin"),
    (ROLE_SUPERUSER, "Superuser"),
]

# MFA states
MFA_STATE_DISABLED: Final[str] = "disabled"
MFA_STATE_ENABLED: Final[str] = "enabled"
MFA_STATE_REQUIRED: Final[str] = "required"
MFA_STATE_CHOICES: Final[list[tuple[str, str]]] = [
    (MFA_STATE_DISABLED, "Disabled"),
    (MFA_STATE_ENABLED, "Enabled"),
    (MFA_STATE_REQUIRED, "Required"),
]

# Token types
TOKEN_TYPE_EMAIL: Final[str] = "email"
TOKEN_TYPE_SMS: Final[str] = "sms"
TOKEN_TYPE_TOTP: Final[str] = "totp"
TOKEN_TYPE_CHOICES: Final[list[tuple[str, str]]] = [
    (TOKEN_TYPE_EMAIL, "Email"),
    (TOKEN_TYPE_SMS, "SMS"),
    (TOKEN_TYPE_TOTP, "TOTP"),
]
