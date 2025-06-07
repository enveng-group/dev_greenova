"""Audit and user-related signals for Greenova core app.

Captures system-wide changes and activities for audit trail.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any

from beartype import beartype
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .audit_utils import log_audit_event
from .models import CustomUser, UserProfile


@receiver(post_save, sender=CustomUser)
@beartype
def user_saved(sender: Any, instance: CustomUser, created: bool, **kwargs: Any) -> None:
    if created:
        log_audit_event(
            user=instance,
            action="user_created",
            object_type="CustomUser",
            object_id=str(instance.pk),
            message="User account created.",
        )
    else:
        log_audit_event(
            user=instance,
            action="user_updated",
            object_type="CustomUser",
            object_id=str(instance.pk),
            message="User account updated.",
        )


@receiver(post_save, sender=UserProfile)
@beartype
def profile_saved(
    sender: Any,
    instance: UserProfile,
    created: bool,
    **kwargs: Any,
) -> None:
    log_audit_event(
        user=instance.user,
        action="profile_saved",
        object_type="UserProfile",
        object_id=str(instance.pk),
        message="User profile saved.",
    )


@receiver(post_delete, sender=CustomUser)
@beartype
def user_deleted(sender: Any, instance: CustomUser, **kwargs: Any) -> None:
    log_audit_event(
        user=None,
        action="user_deleted",
        object_type="CustomUser",
        object_id=str(instance.pk),
        message="User account deleted.",
    )
