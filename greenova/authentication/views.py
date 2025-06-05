# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Authentication service views for the authentication app.

This module provides the AuthenticationService class for managing user
authentication, permission checking, session management, and multi-factor
authentication (MFA), with strict type annotations and runtime type checking.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - AuthenticationService for authentication, permissions, session, and MFA

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from typing import Dict, Any, Optional
from beartype import beartype

from .types import (
    UserInfoDict,
    SessionDataDict,
    MfaPayloadDict,
    Authenticator,
    PermissionChecker,
    SessionManager,
    MfaHandler,
)


class AuthenticationService:
    """Service for user authentication, permission checking, session, and MFA."""

    @beartype
    def __init__(
        self,
        authenticator: Authenticator,
        permission_checker: PermissionChecker,
        session_manager: SessionManager,
        mfa_handler: MfaHandler,
    ) -> None:
        """
        Initialize the AuthenticationService.

        Args:
            authenticator: Authenticator instance for user authentication.
            permission_checker: PermissionChecker instance for permission checks.
            session_manager: SessionManager instance for session handling.
            mfa_handler: MfaHandler instance for MFA handling.
        """
        self.authenticator = authenticator
        self.permission_checker = permission_checker
        self.session_manager = session_manager
        self.mfa_handler = mfa_handler

    @beartype
    def authenticate_user(self, user_info: UserInfoDict) -> Optional[SessionDataDict]:
        """
        Authenticate a user and create a session if successful.

        Args:
            user_info: Dictionary containing user authentication info.

        Returns:
            SessionDataDict if authentication is successful, None otherwise.
        """
        if self.authenticator.authenticate(user_info):
            session_data = self.session_manager.create_session(user_info)
            return session_data
        return None

    @beartype
    def check_permissions(self, session_data: SessionDataDict, resource: str) -> bool:
        """
        Check if the session has permission to access a resource.

        Args:
            session_data: The session data dictionary.
            resource: The resource string to check.

        Returns:
            True if permission is granted, False otherwise.
        """
        return self.permission_checker.check(session_data, resource)

    @beartype
    def handle_mfa(self, mfa_payload: MfaPayloadDict) -> bool:
        """
        Handle multi-factor authentication (MFA) for a user.

        Args:
            mfa_payload: The MFA payload dictionary.

        Returns:
            True if MFA is successful, False otherwise.
        """
        return self.mfa_handler.handle(mfa_payload)
