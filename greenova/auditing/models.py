from django.db import models
from obligations.models import Obligation

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
