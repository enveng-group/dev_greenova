from django.db import models
from obligations.models import Obligation
from mechanisms.models import EnvironmentalMechanism
from django.contrib.auth import get_user_model
User = get_user_model()

class Mitigation(models.Model):
    audit_entry = models.ForeignKey("AuditEntry", on_delete=models.CASCADE, related_name="mitigations")
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("open", "Open"),
            ("closed", "Closed"),
            ("action_required", "Action Required"),
        ],
        default="open"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mitigation for {self.audit_entry}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        audit_entry = self.audit_entry
        if audit_entry.mitigations.exclude(status='closed').exists():
            audit_entry.status = 'noncompliant'
        else:
            audit_entry.status = 'compliant'
        audit_entry.save()

class CorrectiveAction(models.Model):
    mitigation = models.ForeignKey(Mitigation, on_delete=models.CASCADE, related_name="corrective_actions")
    task = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("open", "Open"),
            ("in_progress", "In Progress"),
            ("closed", "Closed"),
            ("overdue", "Overdue"),
        ],
        default="open"
    )
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"CA for {self.mitigation} (Status: {self.status})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        mitigation = self.mitigation
        if mitigation.corrective_actions.exclude(status='closed').exists():
            mitigation.status = 'action_required'
        else:
            mitigation.status = 'closed'
        mitigation.save()

class Audit(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    mechanisms = models.ManyToManyField(EnvironmentalMechanism)

    def generate_entries_from_mechanisms(self):
        obligations = Obligation.objects.filter(
            primary_environmental_mechanism__in=self.mechanisms.all()
        )
        for obligation in obligations:
            AuditEntry.objects.get_or_create(
                audit=self,
                obligation=obligation
            )

class AuditEntry(models.Model):
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name="entries")
    obligation = models.ForeignKey(Obligation, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('compliant', 'Compliant'),
        ('noncompliant', 'Non-Compliant'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    FINDING_CHOICES = [
        ('compliant', 'Compliant'),
        ('noncompliant', 'Non-Compliant'),
        ('not_applicable', 'Not Applicable'),
    ]
    finding = models.CharField(
        max_length=20,
        choices=FINDING_CHOICES,
        default='compliant'
    )

class ComplianceComment(models.Model):
    obligation = models.ForeignKey(
        'obligations.Obligation', 
        on_delete=models.CASCADE, 
        related_name='compliance_comments'
        )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Compliance for {self.obligation.obligation_number}'

class NonConformanceComment(models.Model):
    obligation = models.ForeignKey(
        'obligations.Obligation', 
        on_delete=models.CASCADE, 
        related_name='non_conformance_comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Non-Conformance for {self.obligation.obligation_number}'
