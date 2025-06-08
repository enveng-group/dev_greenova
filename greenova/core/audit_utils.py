"""Audit utilities for Greenova core app.

Provides functions for logging audit events and compliance tracking.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import logging
from typing import Any

from beartype import beartype
from django.utils import timezone

from .models import AuditLog, CustomUser

logger = logging.getLogger(__name__)


@beartype
def log_audit_event(
    user: CustomUser | None,
    action: str,
    object_type: str = "",
    object_id: str = "",
    message: str = "",
    ip_address: str | None = None,
    extra_data: dict[str, Any] | None = None,
) -> None:
    """Log an audit event to the AuditLog model.

    Args:
        user: The user performing the action.
        action: The action performed.
        object_type: The type of object affected.
        object_id: The ID of the object affected.
        message: Additional message or context.
        ip_address: IP address of the user.
        extra_data: Any extra data to log.

    """
    AuditLog.objects.create(
        user=user,
        action=action,
        object_type=object_type,
        object_id=object_id,
        message=message,
        ip_address=ip_address,
        extra_data=extra_data or {},
        timestamp=timezone.now(),
    )
    logger.info(
        "Audit event: user=%s action=%s object_type=%s object_id=%s msg=%s",
        getattr(user, "username", None),
        action,
        object_type,
        object_id,
        message,
    )


@beartype
def get_recent_audit_logs(limit: int = 50) -> list[AuditLog]:
    """Retrieve recent audit logs.

    Args:
        limit: The maximum number of logs to retrieve.

    Returns:
        A list of AuditLog instances.

    """
    return list(AuditLog.objects.select_related("user").order_by("-timestamp")[:limit])
