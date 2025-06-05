# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Authentication user model for the authentication app.

This module provides the AuthUser model for managing authentication users,
with strict type annotations, runtime type checking, and Google style docstrings.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Permissions for object-level access control

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from beartype import beartype
from django.db import models

from .validators import validate_username


@beartype
class AuthUser(models.Model):
    """Authentication user model.

    Attributes:
        id (int): The primary key for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The hashed password of the user.

    """

    id: models.AutoField = models.AutoField(primary_key=True)
    username: models.CharField = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_username],
    )
    email: models.EmailField = models.EmailField(unique=True)
    password: models.CharField = models.CharField(max_length=128)

    # Example usage for role field (if/when added):
    # role: models.CharField = models.CharField(
    #     max_length=20, choices=USER_ROLE_CHOICES, default=ROLE_USER
    # )

    @beartype
    def __str__(self) -> str:
        """Return a string representation of the user.

        Returns:
            str: The username of the user.

        """
        return self.username

    class Meta:
        default_permissions = ("add", "change", "delete", "view")
        # Enable object-level permissions for django-guardian
