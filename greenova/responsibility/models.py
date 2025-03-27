from django.contrib.auth.models import User
from django.db import models

from core.utils.roles import get_responsibility_choices


class Responsibility(models.Model):
    """
    Model representing a responsibility that can be assigned to obligations.
    These values match the responsibility choices in obligations.models.Obligation.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        choices=get_responsibility_choices(),
    )
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Responsibility'
        verbose_name_plural = 'Responsibilities'
        ordering = ['name']

    def __str__(self):
        return self.name
