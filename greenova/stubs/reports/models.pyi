from django.db import models
from typing import ClassVar

class Report(models.Model):
    name: models.CharField
    description: models.TextField
    created_at: models.DateTimeField
    updated_at: models.DateTimeField
    class Meta:
        ordering: ClassVar[list[str]]
        verbose_name: str
        verbose_name_plural: str
    def __str__(self) -> str: ...
