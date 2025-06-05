"""
Custom type definitions and type aliases for the authentication app.

Centralizes reusable type hints and aliases for authentication, permissions,
and session management, and provides Protocols for authenticators, permission
checkers, session managers, and MFA handlers to enable strict type-safety
across modules.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protocols for authenticators, permission checkers, session managers, and MFA handlers

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any, Dict, List, Protocol, TypedDict, runtime_checkable
from beartype import beartype
from django.contrib.auth.models import AbstractUser

class UserInfoDict(TypedDict):
    """TypedDict for user info."""
    id: str
    username: str
    email: str
    is_active: bool
    is_staff: bool
    last_login: str | None
    date_joined: str
    permissions: List[str]

class SessionDataDict(TypedDict):
    """TypedDict for session data."""
    session_key: str
    user_id: str
    created_at: str
    expires_at: str
    data: Dict[str, Any]

class MfaPayloadDict(TypedDict):
    """TypedDict for MFA payload."""
    method: str
    verified: bool
    challenge: str
    attempts: int

PermissionSet = List[str]

@runtime_checkable
class Authenticator(Protocol):
    """Protocol for authenticators."""

    @beartype
    def authenticate(self, credentials: Dict[str, Any]) -> UserInfoDict | None:
        """Authenticate a user with credentials.

        Args:
            credentials: The authentication credentials.

        Returns:
            UserInfoDict | None: The user info dictionary or None if not authenticated.
        """
        ...

@runtime_checkable
class PermissionChecker(Protocol):
    """Protocol for permission checking."""

    @beartype
    def __call__(self, user: AbstractUser, perm: str) -> bool:
        """Check if a user has a permission.

        Args:
            user: The user instance.
            perm: The permission string.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        ...

@runtime_checkable
class SessionManager(Protocol):
    """Protocol for session management."""

    @beartype
    def create_session(self, user: UserInfoDict) -> SessionDataDict:
        """Create a session for a user.

        Args:
            user: The user info dictionary.

        Returns:
            SessionDataDict: The session data dictionary.
        """
        ...

    @beartype
    def validate_session(self, session_key: str) -> bool:
        """Validate a session key.

        Args:
            session_key: The session key.

        Returns:
            bool: True if the session is valid, False otherwise.
        """
        ...

    @beartype
    def destroy_session(self, session_key: str) -> None:
        """Destroy a session by its key.

        Args:
            session_key: The session key.
        """
        ...

@runtime_checkable
class MfaHandler(Protocol):
    """Protocol for multi-factor authentication handlers."""

    @beartype
    def initiate(self, user: UserInfoDict) -> MfaPayloadDict:
        """Initiate an MFA challenge for a user.

        Args:
            user: The user info dictionary.

        Returns:
            MfaPayloadDict: The MFA payload dictionary.
        """
        ...

    @beartype
    def verify(self, user: UserInfoDict, payload: MfaPayloadDict) -> bool:
        """Verify an MFA challenge for a user.

        Args:
            user: The user info dictionary.
            payload: The MFA payload dictionary.

        Returns:
            bool: True if verification is successful, False otherwise.
        """
        ...
