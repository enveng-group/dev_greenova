"""
Custom type definitions and type aliases for the users app.

Centralizes reusable type hints and aliases for user profiles, permissions,
and session data, and provides Protocols for user profile managers, permission
managers, and session managers to enable strict type-safety across modules.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protocols for user profile managers, permission managers, and session managers

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any, List, Protocol, TypedDict, runtime_checkable
from beartype import beartype

class UserProfileDict(TypedDict):
    """TypedDict for user profile data."""
    id: str
    username: str
    email: str
    is_active: bool
    is_staff: bool
    date_joined: str
    last_login: str | None
    roles: List[str]

class UserPermissionsDict(TypedDict):
    """TypedDict for user permissions."""
    user_id: str
    permissions: List[str]

class SessionDataDict(TypedDict):
    """TypedDict for session data."""
    session_key: str
    user_id: str
    created_at: str
    expires_at: str
    data: dict[str, Any]

@runtime_checkable
class UserProfileManager(Protocol):
    """Protocol for managing user profiles."""

    @beartype
    def get_profile(self, user_id: str) -> UserProfileDict:
        """Retrieve a user profile by user ID.

        Args:
            user_id: The unique identifier for the user.

        Returns:
            UserProfileDict: The user profile dictionary.
        """
        ...

    @beartype
    def update_profile(self, user_id: str, data: UserProfileDict) -> None:
        """Update a user profile.

        Args:
            user_id: The unique identifier for the user.
            data: The updated user profile dictionary.
        """
        ...

@runtime_checkable
class PermissionManager(Protocol):
    """Protocol for managing user permissions."""

    @beartype
    def get_permissions(self, user_id: str) -> UserPermissionsDict:
        """Retrieve permissions for a user.

        Args:
            user_id: The unique identifier for the user.

        Returns:
            UserPermissionsDict: The user permissions dictionary.
        """
        ...

    @beartype
    def set_permissions(self, user_id: str, permissions: List[str]) -> None:
        """Set permissions for a user.

        Args:
            user_id: The unique identifier for the user.
            permissions: The list of permissions to assign.
        """
        ...

@runtime_checkable
class UserSessionManager(Protocol):
    """Protocol for managing user sessions."""

    @beartype
    def create_session(self, user_id: str) -> SessionDataDict:
        """Create a new session for a user.

        Args:
            user_id: The unique identifier for the user.

        Returns:
            SessionDataDict: The created session data dictionary.
        """
        ...

    @beartype
    def validate_session(self, session_key: str) -> bool:
        """Validate a session key.

        Args:
            session_key: The session key to validate.

        Returns:
            bool: True if the session is valid, False otherwise.
        """
        ...

    @beartype
    def destroy_session(self, session_key: str) -> None:
        """Destroy a session by its key.

        Args:
            session_key: The session key to destroy.
        """
        ...
