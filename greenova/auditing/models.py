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
from typing import TYPE_CHECKING, Any, ClassVar

from django.contrib.auth import get_user_model
from django.db import models
from mechanisms.models import EnvironmentalMechanism
from obligations.models import Obligation

from .constants import (
    CORRECTIVE_ACTION_STATUS_CHOICES,
    CORRECTIVE_ACTION_STATUS_OPEN,
    MITIGATION_STATUS_CHOICES,
    MITIGATION_STATUS_OPEN,
)
from .validators import validate_non_empty_description

if TYPE_CHECKING:
    from django.db.models import QuerySet

try:
    from pb_model.models import ProtoBufMixin
except ImportError:
    ProtoBufMixin: type[models.Model] = models.Model  # type: ignore

try:
    from greenova.protobuf.auditing_pb2 import (
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


class Mitigation(ProtoBufMixin, models.Model):
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
        validators=[validate_non_empty_description],
    )
    status: models.CharField = models.CharField(
        max_length=20,
        choices=MITIGATION_STATUS_CHOICES,
        default=MITIGATION_STATUS_OPEN,
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return string representation of the mitigation.

        Returns:
            Human-readable string for the mitigation.

        """
        return f"Mitigation for {self.audit_entry}"

    # Status update logic is now handled via post_save signal in signals.py

    class Meta:
        verbose_name = "Mitigation"
        default_permissions = ("add", "change", "delete", "view")
        # Enable object-level permissions for django-guardian


class CorrectiveAction(ProtoBufMixin, models.Model):
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

    def __str__(self) -> str:
        """Return string representation of the corrective action.

        Returns:
            Human-readable string for the corrective action.

        """
        return f"CA for {self.mitigation} (Status: {self.status})"

    # Status update logic is now handled via post_save signal in signals.py

    class Meta:
        verbose_name = "Corrective Action"
        default_permissions = ("add", "change", "delete", "view")
        # Enable object-level permissions for django-guardian


class Audit(ProtoBufMixin):
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
        EnvironmentalMechanism,
    )

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


class AuditEntry(ProtoBufMixin):
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
        Audit,
        on_delete=models.CASCADE,
        related_name="entries",
    )
    obligation: models.ForeignKey = models.ForeignKey(
        Obligation,
        on_delete=models.CASCADE,
    )
    STATUS_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("pending", "Pending"),
        ("compliant", "Compliant"),
        ("noncompliant", "Non-Compliant"),
    ]
    status: models.CharField = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
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


class ComplianceComment(ProtoBufMixin):
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

    def __str__(self) -> str:
        """Return string representation of the compliance comment.

        Returns:
            Human-readable string for the compliance comment.

        """
        return f"Compliance for {self.obligation.obligation_number}"


class NonConformanceComment(ProtoBufMixin):
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

    def __str__(self) -> str:
        """Return string representation of the non-conformance comment.

        Returns:
            Human-readable string for the non-conformance comment.

        """
        return f"Non-Conformance for {self.obligation.obligation_number}"
