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

import os

from beartype import beartype
from django.contrib.auth.models import User
from django.db import models
from django_lifecycle import AFTER_SAVE, LifecycleModel, hook
from PIL import Image

try:
    from pb_model.models import ProtoBufMixin
except ImportError:
    ProtoBufMixin = models.Model  # fallback for type checking

try:
    from .proto.users_pb2 import ProfileProto
except ImportError:
    ProfileProto = None

from .validators import validate_phone_number
from .types import (
    UserProfileDict,
    UserPermissionsDict,
    SessionDataDict,
    UserProfileManager,
    PermissionManager,
    UserSessionManager,
)


@beartype
class Profile(LifecycleModel, ProtoBufMixin):
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
        permissions = [
            ("view_profile", "Can view profile"),
            ("change_profile", "Can change profile"),
            ("delete_profile", "Can delete profile"),
        ]
        default_permissions = ("add", "change", "delete", "view")
        # Enable object-level permissions for django-guardian

    @beartype
    def __str__(self) -> str:
        """Returns a string representation of the Profile instance.

        Returns:
            str: The username's profile string.
        """
        return f"{self.user.username}'s profile"

    @beartype
    @hook(AFTER_SAVE)
    def process_profile_image(self) -> None:
        """Resize and create thumbnail for profile image after save.

        If the profile image exceeds 400x400 pixels, it is resized to fit within
        these dimensions. Additionally, a thumbnail of 100x100 pixels is created
        and saved alongside the original image.

        Raises:
            Exception: If image processing fails.
        """
        if self.profile_image:
            try:
                img_path = self.profile_image.path
                img = Image.open(img_path)
                max_size = (400, 400)
                if img.height > 400 or img.width > 400:
                    img.thumbnail(max_size)
                    img.save(img_path)
                thumb_path = os.path.join(
                    os.path.dirname(img_path),
                    f"thumb_{os.path.basename(img_path)}",
                )
                img.thumbnail((100, 100))
                img.save(thumb_path)
            except Exception as e:
                import logging

                logger = logging.getLogger(__name__)
                logger.warning("Profile image processing failed: %s", e)
