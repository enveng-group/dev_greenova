from typing import Optional

from core.utils.roles import get_responsibility_choices
from django.db import models
from django.db.models import CharField, TextField


class Responsibility(models.Model):
    """
    Model representing a responsibility role that can be assigned to users
    for specific obligations.
    """

    name: CharField = models.CharField(
        max_length=255,
        unique=True,
        choices=get_responsibility_choices(),
    )
    description: Optional[TextField] = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'obligation', 'role']
        ordering = ['-created_at']
        verbose_name = 'Responsibility Assignment'
        verbose_name_plural = 'Responsibility Assignments'

    def __str__(self):
        return str(self.name)
