"""Auditing models for environmental compliance management.

This module defines Django ORM models for audit processes, including
Mitigation, CorrectiveAction, Audit, AuditEntry, ComplianceComment,
and NonConformanceComment. All models use strict type annotations,
Google style docstrings, and runtime type checking with beartype.

Author:
    Adrian Gallo <agallo@enveng-group.com.au>

License:
    AGPL-3.0
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar, Optional, Type

from beartype import beartype
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet
from django_lifecycle import AFTER_SAVE, LifecycleModel, hook
from mechanisms.models import EnvironmentalMechanism
from obligations.models import Obligation

from .constants import (
    CORRECTIVE_ACTION_STATUS_CHOICES,
    CORRECTIVE_ACTION_STATUS_CLOSED,
    CORRECTIVE_ACTION_STATUS_OPEN,
    MITIGATION_STATUS_ACTION_REQUIRED,
    MITIGATION_STATUS_CHOICES,
    MITIGATION_STATUS_CLOSED,
    MITIGATION_STATUS_OPEN,
)
from .validators import validate_non_empty_description
from .types import AuditRecordDict, AuditEntryDict

try:
    from pb_model.models import ProtoBufMixin
except ImportError:
    ProtoBufMixin: Type[models.Model] = models.Model  # type: ignore

try:
    from .proto.auditing_pb2 import (
        AuditEntryProto,
        AuditProto,
        ComplianceCommentProto,
        CorrectiveActionProto,
        MitigationProto,
        NonConformanceCommentProto,
    )
except ImportError:
    MitigationProto = None
    CorrectiveActionProto = None
    AuditProto = None
    AuditEntryProto = None
    ComplianceCommentProto = None
    NonConformanceCommentProto = None

User = get_user_model()
logger = logging.getLogger(__name__)


@beartype
class Mitigation(LifecycleModel, ProtoBufMixin):
    """Model representing a mitigation for an audit entry.

    Attributes:
        pb_model: Protobuf model for serialization.
        audit_entry: Related AuditEntry instance.
        description: Description of the mitigation.
        status: Status of the mitigation.
        created_at: Timestamp of creation.
    """

    pb_model: ClassVar[Any] = MitigationProto

    audit_entry: models.ForeignKey = models.ForeignKey(
        "AuditEntry",
        on_delete=models.CASCADE,
        related_name="mitigations",
    )
    description: models.TextField = models.TextField(
        validators=[validate_non_empty_description]
    )
    status: models.CharField = models.CharField(
        max_length=20,
        choices=MITIGATION_STATUS_CHOICES,
        default=MITIGATION_STATUS_OPEN,
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    @beartype
    def __str__(self) -> str:
        """Return string representation of the mitigation.

        Returns:
            Human-readable string for the mitigation.
        """
        return f"Mitigation for {self.audit_entry}"

    @hook(AFTER_SAVE)
    @beartype
    def update_audit_entry_status_lifecycle(self) -> None:
        """Lifecycle hook: update audit entry status after saving mitigation.

        Updates the related AuditEntry status based on the status of all
        associated mitigations.
        """
        audit_entry = self.audit_entry
        if audit_entry.mitigations.exclude(
            status=MITIGATION_STATUS_CLOSED
        ).exists():
            audit_entry.status = "noncompliant"
        else:
            audit_entry.status = "compliant"
        audit_entry.save()
        logger.info(
            "AuditEntry %s status updated by Mitigation lifecycle hook",
            audit_entry.id,
        )

    class Meta:
        verbose_name = "Mitigation"
        permissions = [
            ("view_mitigation", "Can view mitigation"),
            ("change_mitigation", "Can change mitigation"),
            ("delete_mitigation", "Can delete mitigation"),
        ]
        default_permissions = ("add", "change", "delete", "view")
        # Enable object-level permissions for django-guardian


@beartype
class CorrectiveAction(LifecycleModel, ProtoBufMixin):
    """Model representing a corrective action for a mitigation.

    Attributes:
        pb_model: Protobuf model for serialization.
        mitigation: Related Mitigation instance.
        task: Description of the corrective action.
        status: Status of the corrective action.
        assigned_to: User assigned to the action.
        created_at: Timestamp of creation.
        due_date: Due date for the action.
    """

    pb_model: ClassVar[Any] = CorrectiveActionProto

    mitigation: models.ForeignKey = models.ForeignKey(
        Mitigation,
        on_delete=models.CASCADE,
        related_name="corrective_actions",
    )
    task: models.TextField = models.TextField()
    status: models.CharField = models.CharField(
        max_length=20,
        choices=CORRECTIVE_ACTION_STATUS_CHOICES,
        default=CORRECTIVE_ACTION_STATUS_OPEN,
    )
    assigned_to: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    due_date: models.DateField = models.DateField(null=True, blank=True)

    @beartype
    def __str__(self) -> str:
        """Return string representation of the corrective action.

        Returns:
            Human-readable string for the corrective action.
        """
        return f"CA for {self.mitigation} (Status: {self.status})"

    @hook(AFTER_SAVE)
    @beartype
    def update_mitigation_status_lifecycle(self) -> None:
        """Lifecycle hook: update mitigation status after saving corrective action.

        Updates the related Mitigation status based on the status of all
        associated corrective actions.
        """
        mitigation = self.mitigation
        if mitigation.corrective_actions.exclude(
            status=CORRECTIVE_ACTION_STATUS_CLOSED
        ).exists():
            mitigation.status = MITIGATION_STATUS_ACTION_REQUIRED
        else:
            mitigation.status = MITIGATION_STATUS_CLOSED
        mitigation.save()
        logger.info(
            "Mitigation %s status updated by CorrectiveAction lifecycle hook",
            mitigation.id,
        )

    class Meta:
        verbose_name = "Corrective Action"
        permissions = [
            ("view_correctiveaction", "Can view corrective action"),
            ("change_correctiveaction", "Can change corrective action"),
            ("delete_correctiveaction", "Can delete corrective action"),
        ]
        default_permissions = ("add", "change", "delete", "view")
        # Enable object-level permissions for django-guardian


@beartype
class Audit(LifecycleModel, ProtoBufMixin):
    """Audit model for environmental compliance audits.

    Attributes:
        pb_model: Protobuf model for serialization.
        name: Name of the audit.
        created_at: Timestamp of creation.
        mechanisms: Related environmental mechanisms.
    """

    pb_model: ClassVar[Any] = AuditProto

    name: models.CharField = models.CharField(max_length=255)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    mechanisms: models.ManyToManyField = models.ManyToManyField(
        EnvironmentalMechanism
    )

    @beartype
    def generate_entries_from_mechanisms(self) -> None:
        """Generate audit entries for all obligations related to mechanisms.

        Creates AuditEntry objects for each obligation linked to the audit's
        mechanisms.
        """
        obligations: QuerySet[Obligation] = Obligation.objects.filter(
            primary_environmental_mechanism__in=self.mechanisms.all(),
        )
        for obligation in obligations:
            AuditEntry.objects.get_or_create(
                audit=self,
                obligation=obligation,
            )


@beartype
class AuditEntry(LifecycleModel, ProtoBufMixin):
    """Audit entry for a specific obligation in an audit.

    Attributes:
        pb_model: Protobuf model for serialization.
        audit: Related Audit instance.
        obligation: Related Obligation instance.
        status: Status of the audit entry.
        finding: Finding for the audit entry.
    """

    pb_model: ClassVar[Any] = AuditEntryProto

    audit: models.ForeignKey = models.ForeignKey(
        Audit, on_delete=models.CASCADE, related_name="entries"
    )
    obligation: models.ForeignKey = models.ForeignKey(
        Obligation, on_delete=models.CASCADE
    )
    STATUS_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("pending", "Pending"),
        ("compliant", "Compliant"),
        ("noncompliant", "Non-Compliant"),
    ]
    status: models.CharField = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    FINDING_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("compliant", "Compliant"),
        ("noncompliant", "Non-Compliant"),
        ("not_applicable", "Not Applicable"),
    ]
    finding: models.CharField = models.CharField(
        max_length=20,
        choices=FINDING_CHOICES,
        default="compliant",
    )


@beartype
class ComplianceComment(LifecycleModel, ProtoBufMixin):
    """Comment for compliance on an obligation.

    Attributes:
        pb_model: Protobuf model for serialization.
        obligation: Related Obligation instance.
        text: Comment text.
        created_at: Timestamp of creation.
    """

    pb_model: ClassVar[Any] = ComplianceCommentProto

    obligation: models.ForeignKey = models.ForeignKey(
        "obligations.Obligation",
        on_delete=models.CASCADE,
        related_name="compliance_comments",
    )
    text: models.TextField = models.TextField()
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    @beartype
    def __str__(self) -> str:
        """Return string representation of the compliance comment.

        Returns:
            Human-readable string for the compliance comment.
        """
        return f"Compliance for {self.obligation.obligation_number}"


@beartype
class NonConformanceComment(LifecycleModel, ProtoBufMixin):
    """Comment for non-conformance on an obligation.

    Attributes:
        pb_model: Protobuf model for serialization.
        obligation: Related Obligation instance.
        text: Comment text.
        created_at: Timestamp of creation.
    """

    pb_model: ClassVar[Any] = NonConformanceCommentProto

    obligation: models.ForeignKey = models.ForeignKey(
        "obligations.Obligation",
        on_delete=models.CASCADE,
        related_name="non_conformance_comments",
    )
    text: models.TextField = models.TextField()
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    @beartype
    def __str__(self) -> str:
        """Return string representation of the non-conformance comment.

        Returns:
            Human-readable string for the non-conformance comment.
        """
        return f"Non-Conformance for {self.obligation.obligation_number}"
