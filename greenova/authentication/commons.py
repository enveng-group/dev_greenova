# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Common authentication utilities for the authentication app.

This module provides the AuthenticationService class for managing user
permissions and authentication logic, with strict type annotations and
runtime type checking.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - AuthenticationService for user permission management

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from typing import Dict
from beartype import beartype

from .types import UserInfoDict, PermissionSet


class AuthenticationService:
    """Service for managing user permissions and authentication."""

    @beartype
    def __init__(self) -> None:
        """Initialize the AuthenticationService with an empty permissions dict."""
        self.user_permissions: Dict[str, PermissionSet] = {}

    @beartype
    def add_user(self, user_info: UserInfoDict) -> None:
        """Add a user and their permissions to the service.

        Args:
            user_info: Dictionary containing user_id and permissions.
        """
        user_id = user_info["user_id"]
        permissions = user_info["permissions"]
        self.user_permissions[user_id] = permissions

    @beartype
    def check_permission(self, user_id: str, permission: str) -> bool:
        """Check if a user has a specific permission.

        Args:
            user_id: The user's unique identifier.
            permission: The permission string to check.

        Returns:
            True if the user has the permission, False otherwise.
        """
        if user_id not in self.user_permissions:
            return False
        return permission in self.user_permissions[user_id]
