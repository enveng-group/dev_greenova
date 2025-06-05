"""Signal handlers for the auditing app.

This module contains Django signal handlers for Mitigation and CorrectiveAction models.
Implements logic previously handled by django-lifecycle hooks.

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging

from beartype import beartype
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import (
    CORRECTIVE_ACTION_STATUS_CLOSED,
    MITIGATION_STATUS_ACTION_REQUIRED,
    MITIGATION_STATUS_CLOSED,
)
from .models import CorrectiveAction, Mitigation

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Mitigation)
@beartype
def update_audit_entry_status(sender, instance: Mitigation, **kwargs) -> None:
    """Update AuditEntry status after saving Mitigation (migrated from lifecycle hook)."""
    audit_entry = instance.audit_entry
    if audit_entry.mitigations.exclude(status=MITIGATION_STATUS_CLOSED).exists():
        audit_entry.status = "noncompliant"
    else:
        audit_entry.status = "compliant"
    audit_entry.save()
    logger.info("AuditEntry %s status updated by Mitigation signal", audit_entry.id)


@receiver(post_save, sender=CorrectiveAction)
@beartype
def update_mitigation_status(sender, instance: CorrectiveAction, **kwargs) -> None:
    """Update Mitigation status after saving CorrectiveAction (migrated from lifecycle hook)."""
    mitigation = instance.mitigation
    if mitigation.corrective_actions.exclude(
        status=CORRECTIVE_ACTION_STATUS_CLOSED,
    ).exists():
        mitigation.status = MITIGATION_STATUS_ACTION_REQUIRED
    else:
        mitigation.status = MITIGATION_STATUS_CLOSED
    mitigation.save()
    logger.info(
        "Mitigation %s status updated by CorrectiveAction signal",
        mitigation.id,
    )
