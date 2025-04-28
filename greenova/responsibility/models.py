from typing import Optional

from core.utils.roles import get_responsibility_choices
from django.conf import settings
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
        verbose_name = 'Responsibility'
        verbose_name_plural = 'Responsibilities'

    def __str__(self):
        return str(self.name)


class ResponsibilityAssignment(models.Model):
    """
    Model representing an assignment of a responsibility to a user.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='responsibility_assignments'
    )
    responsibility = models.ForeignKey(
        Responsibility,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    obligation = models.ForeignKey(
        'obligations.Obligation',
        on_delete=models.CASCADE,
        related_name='responsibility_assignments'
    )
    role = models.ForeignKey(
        Responsibility,
        on_delete=models.CASCADE,
        related_name='role_assignments'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_responsibility_assignments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Responsibility Assignment'
        verbose_name_plural = 'Responsibility Assignments'
        ordering = ['-created_at']
        unique_together = ['user', 'obligation', 'role']

    def __str__(self):
        return f"{self.user} - {self.role} for {self.obligation}"
