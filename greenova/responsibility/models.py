from typing import Optional

from core.utils.roles import get_responsibility_choices
from django.db import models
from django.db.models import CharField, TextField


class Responsibility(models.Model):
    """
    Model representing a responsibility that can be assigned to obligations.
    These values match the responsibility choices in obligations.models.Obligation.
    """

    name: CharField = models.CharField(
        max_length=255,
        unique=True,
        choices=get_responsibility_choices(),
    )
    description: Optional[TextField] = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Responsibility'
        verbose_name_plural = 'Responsibilities'
        ordering = ['name']

    def __str__(self):
        return str(self.name)
