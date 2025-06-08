"""Audit and user-related signals for Greenova core app.

Captures system-wide changes and activities for audit trail.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any

from beartype import beartype
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .audit_utils import log_audit_event
from .models import CustomUser, UserProfile

User = get_user_model()


@receiver(post_save, sender=CustomUser)
@beartype
def user_saved(
    sender: type[CustomUser], instance: CustomUser, created: bool, **kwargs: Any
) -> None:
    """Log audit event when a CustomUser is created or updated."""
    action = "created" if created else "updated"
    log_audit_event(
        user=instance,
        action=f"user_{action}",
        object_type="CustomUser",
        object_id=str(instance.pk),
        message=f"User {action}: {instance.username}",
    )


@receiver(post_delete, sender=CustomUser)
@beartype
def user_deleted(sender: type[CustomUser], instance: CustomUser, **kwargs: Any) -> None:
    """Log audit event when a CustomUser is deleted."""
    log_audit_event(
        user=None,
        action="user_deleted",
        object_type="CustomUser",
        object_id=str(instance.pk),
        message=f"User deleted: {instance.username}",
    )


@receiver(post_save, sender=UserProfile)
@beartype
def profile_saved(
    sender: type[UserProfile], instance: UserProfile, created: bool, **kwargs: Any
) -> None:
    """Log audit event when a UserProfile is created or updated."""
    action = "created" if created else "updated"
    log_audit_event(
        user=instance.user,
        action=f"profile_{action}",
        object_type="UserProfile",
        object_id=str(instance.pk),
        message=f"Profile {action} for user: {instance.user.username}",
    )


@receiver(post_delete, sender=UserProfile)
@beartype
def profile_deleted(
    sender: type[UserProfile], instance: UserProfile, **kwargs: Any
) -> None:
    """Log audit event when a UserProfile is deleted."""
    log_audit_event(
        user=None,
        action="profile_deleted",
        object_type="UserProfile",
        object_id=str(instance.pk),
        message=f"Profile deleted for user: {instance.user.username}",
    )
