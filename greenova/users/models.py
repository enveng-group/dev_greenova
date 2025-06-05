# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""User profile models for the users app.

This module provides the Profile model, which extends the default Django User
model with additional fields and Protocol Buffer integration. It includes
runtime type checking, Google style docstrings, and image processing logic.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protobuf3 integration for user profiles
    - Image resizing and thumbnail creation on save

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from beartype import beartype
from django.contrib.auth.models import User
from django.db import models

try:
    from pb_model.models import ProtoBufMixin
except ImportError:
    ProtoBufMixin = models.Model  # fallback for type checking

try:
    from .proto.users_pb2 import ProfileProto
except ImportError:
    ProfileProto = None

from .validators import validate_phone_number


class Profile(ProtoBufMixin, models.Model):
    """User profile model extending the default Django User model.

    Attributes:
        pb_model: The protobuf model associated with the Profile.
        user: A one-to-one relationship to the Django User model.
        bio: A text field for the user's biography.
        position: A char field for the user's position.
        department: A char field for the user's department.
        phone_number: A char field for the user's phone number.
        profile_image: An image field for the user's profile picture.
        welcome_email_sent: A boolean field indicating if a welcome email was sent.
        created_at: A datetime field for the creation timestamp.
        updated_at: A datetime field for the last update timestamp.

    """

    pb_model = ProfileProto

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.TextField(max_length=500, blank=True)
    position = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[validate_phone_number],
    )
    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True,
    )
    welcome_email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Removed explicit view/change/delete permissions to avoid clash with builtins
        default_permissions = ("add", "change", "delete", "view")
        # Enable object-level permissions for django-guardian

    @beartype
    def __str__(self) -> str:
        """Returns a string representation of the Profile instance.

        Returns:
            str: The username's profile string.

        """
        return f"{self.user.username}'s profile"

    # Profile image processing is now handled via post_save signal in signals.py
