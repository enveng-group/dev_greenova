"""Models for the Greenova core app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

import logging

from beartype import beartype
from django.contrib.auth.models import AbstractUser
from django.db import models

logger = logging.getLogger(__name__)


class EnvironmentalObligation(models.Model):
    """Model representing an environmental obligation in Greenova.

    Attributes:
        name: The name of the obligation.
        description: A description of the obligation.
        due_date: The due date for the obligation.
        is_complete: Whether the obligation is complete.
        created_at: Timestamp when the obligation was created.
        updated_at: Timestamp when the obligation was last updated.

    """

    name = models.CharField(max_length=255)  # type: ignore[assignment]
    description = models.TextField(blank=True)  # type: ignore[assignment]
    due_date = models.DateField()  # type: ignore[assignment]
    is_complete = models.BooleanField(default=False)  # type: ignore[assignment]
    created_at = models.DateTimeField(auto_now_add=True)  # type: ignore[assignment]
    updated_at = models.DateTimeField(auto_now=True)  # type: ignore[assignment]

    @beartype
    def __str__(self) -> str:  # type: ignore[no-any-return]
        """Return a string representation of the obligation."""
        return str(self.name)


class CustomUser(AbstractUser):
    """Custom user model for Greenova, extending AbstractUser.

    Attributes:
        email: The user's email address (unique).
        is_mfa_enabled: Whether multi-factor authentication is enabled.
        company: Optional company name for the user.

    """

    email = models.EmailField(unique=True)  # type: ignore[assignment]
    is_mfa_enabled = models.BooleanField(default=False)  # type: ignore[assignment]
    company = models.CharField(max_length=255, blank=True)  # type: ignore[assignment]

    @beartype
    def __str__(self) -> str:  # type: ignore[no-any-return]
        """Return a string representation of the user."""
        return str(self.username)


class UserProfile(models.Model):
    """Profile model for extended user information in Greenova.

    Attributes:
        user: The related CustomUser instance.
        display_name: The display name for the user.
        preferences: JSON field for user preferences.
        avatar: Optional avatar image.
        updated_at: Timestamp when the profile was last updated.

    """

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profile",
    )  # type: ignore[assignment]
    display_name = models.CharField(
        max_length=255,
        blank=True)  # type: ignore[assignment]
    preferences = models.JSONField(default=dict, blank=True)  # type: ignore[assignment]
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True)  # type: ignore[assignment]
    updated_at = models.DateTimeField(auto_now=True)  # type: ignore[assignment]

    @beartype
    def __str__(self) -> str:  # type: ignore[no-any-return]
        """Return a string representation of the user profile."""
        return str(self.display_name or self.user.username)


class AuditLog(models.Model):
    """Audit log entry for system-wide audit trails in Greenova.

    Attributes:
        user: The user who performed the action.
        action: The action performed (e.g., 'login', 'update_profile').
        object_type: The type of object affected.
        object_id: The ID of the object affected.
        message: A human-readable message describing the event.
        timestamp: When the event occurred.
        ip_address: The IP address of the user.
        extra_data: Additional data (JSON).

    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )  # type: ignore[assignment]
    action = models.CharField(max_length=64)  # type: ignore[assignment]
    object_type = models.CharField(
        max_length=64,
        blank=True)  # type: ignore[assignment]
    object_id = models.CharField(max_length=64, blank=True)  # type: ignore[assignment]
    message = models.TextField(blank=True)  # type: ignore[assignment]
    timestamp = models.DateTimeField(auto_now_add=True)  # type: ignore[assignment]
    ip_address = models.GenericIPAddressField(
        blank=True, null=True)  # type: ignore[assignment]
    extra_data = models.JSONField(default=dict, blank=True)  # type: ignore[assignment]

    @beartype
    def __str__(self) -> str:  # type: ignore[no-any-return]
        """Return a string representation of the audit log entry."""
        return f"{self.timestamp} {self.user} {self.action} {self.object_type}"

    class Meta:
        verbose_name = "Audit Log Entry"
        verbose_name_plural = "Audit Log Entries"
        ordering = ["-timestamp"]
