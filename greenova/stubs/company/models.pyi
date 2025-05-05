from typing import Optional

from django.db import models

class Company(models.Model):
    name: str
    description: Optional[str]
    website: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    created_at: models.DateTimeField
    updated_at: models.DateTimeField

    class Meta:
        verbose_name_plural: str = "Companies"

    def __str__(self) -> str: ...
