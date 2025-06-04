from beartype import beartype
from django.contrib.auth import get_user_model
from django.db import models
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

try:
    from pb_model.models import ProtoBufMixin
except ImportError:
    ProtoBufMixin = models.Model  # fallback for type checking

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


@beartype
class Mitigation(LifecycleModel, ProtoBufMixin):
    """Model representing a mitigation for an audit entry."""

    pb_model = MitigationProto

    audit_entry = models.ForeignKey(
        "AuditEntry",
        on_delete=models.CASCADE,
        related_name="mitigations",
    )
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=MITIGATION_STATUS_CHOICES,
        default=MITIGATION_STATUS_OPEN,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Mitigation for {self.audit_entry}"

    @hook(AFTER_SAVE)
    def update_audit_entry_status(self) -> None:
        """Update audit entry status after saving mitigation."""
        audit_entry = self.audit_entry
        if audit_entry.mitigations.exclude(status=MITIGATION_STATUS_CLOSED).exists():
            audit_entry.status = "noncompliant"
        else:
            audit_entry.status = "compliant"
        audit_entry.save()

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
    """Model representing a corrective action for a mitigation."""

    pb_model = CorrectiveActionProto

    mitigation = models.ForeignKey(
        Mitigation,
        on_delete=models.CASCADE,
        related_name="corrective_actions",
    )
    task = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=CORRECTIVE_ACTION_STATUS_CHOICES,
        default=CORRECTIVE_ACTION_STATUS_OPEN,
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"CA for {self.mitigation} (Status: {self.status})"

    @hook(AFTER_SAVE)
    def update_mitigation_status(self) -> None:
        """Update mitigation status after saving corrective action."""
        mitigation = self.mitigation
        if mitigation.corrective_actions.exclude(
            status=CORRECTIVE_ACTION_STATUS_CLOSED,
        ).exists():
            mitigation.status = MITIGATION_STATUS_ACTION_REQUIRED
        else:
            mitigation.status = MITIGATION_STATUS_CLOSED
        mitigation.save()

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
    """Audit model for environmental compliance audits."""

    pb_model = AuditProto

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    mechanisms = models.ManyToManyField(EnvironmentalMechanism)

    def generate_entries_from_mechanisms(self) -> None:
        """Generate audit entries for all obligations related to mechanisms."""
        obligations = Obligation.objects.filter(
            primary_environmental_mechanism__in=self.mechanisms.all(),
        )
        for obligation in obligations:
            AuditEntry.objects.get_or_create(
                audit=self,
                obligation=obligation,
            )


@beartype
class AuditEntry(LifecycleModel, ProtoBufMixin):
    """Audit entry for a specific obligation in an audit."""

    pb_model = AuditEntryProto

    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name="entries")
    obligation = models.ForeignKey(Obligation, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("compliant", "Compliant"),
        ("noncompliant", "Non-Compliant"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    FINDING_CHOICES = [
        ("compliant", "Compliant"),
        ("noncompliant", "Non-Compliant"),
        ("not_applicable", "Not Applicable"),
    ]
    finding = models.CharField(
        max_length=20,
        choices=FINDING_CHOICES,
        default="compliant",
    )


@beartype
class ComplianceComment(LifecycleModel, ProtoBufMixin):
    """Comment for compliance on an obligation."""

    pb_model = ComplianceCommentProto

    obligation = models.ForeignKey(
        "obligations.Obligation",
        on_delete=models.CASCADE,
        related_name="compliance_comments",
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Compliance for {self.obligation.obligation_number}"


@beartype
class NonConformanceComment(LifecycleModel, ProtoBufMixin):
    """Comment for non-conformance on an obligation."""

    pb_model = NonConformanceCommentProto

    obligation = models.ForeignKey(
        "obligations.Obligation",
        on_delete=models.CASCADE,
        related_name="non_conformance_comments",
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Non-Conformance for {self.obligation.obligation_number}"
