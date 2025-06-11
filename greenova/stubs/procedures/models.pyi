from _typeshed import Incomplete
from django.db import models
from typing import ClassVar

logger: Incomplete

class Procedure(models.Model):
    STATUS_CHOICES: ClassVar[list]
    COMPLIANCE_STATUSES: ClassVar[list]
    name: models.CharField
    document_id: models.CharField
    project: models.ForeignKey
    version: models.CharField
    description: models.TextField
    status: models.CharField
    compliance_status: models.CharField
    created_at: models.DateTimeField
    updated_at: models.DateTimeField
    effective_date: models.DateField
    review_date: models.DateField
    completed_at: models.DateTimeField
    document_file: models.FileField
    is_active: models.BooleanField
    tags: models.CharField
    class Meta:
        ordering: Incomplete
        verbose_name: str
        verbose_name_plural: str
        indexes: Incomplete
    def __str__(self) -> str: ...
    def mark_as_completed(self) -> None: ...
    def set_status(self, status: str) -> None: ...
    def is_due_for_review(self) -> bool: ...
