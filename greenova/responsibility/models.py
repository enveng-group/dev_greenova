from typing import Any, Optional

from core.utils.roles import get_responsibility_choices
from django.conf import settings
from django.db import models


class Responsibility(models.Model):
    """
    Model representing a responsibility role that can be assigned to users
    for specific obligations.
    """

    name: Any = models.CharField(
        max_length=255,
        choices=get_responsibility_choices(),
    )
    description: Optional[Any] = models.TextField(blank=True)
    company: Any = models.ForeignKey(
        'company.Company',
        on_delete=models.CASCADE,
        related_name='responsibilities',
        null=True,
        blank=True
    )
    is_active: Any = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Responsibility'
        verbose_name_plural = 'Responsibilities'
        unique_together = ['name', 'company']

    def __str__(self) -> str:
        if self.company:
            return f"{self.name} ({self.company.name})"
        return str(self.name)


class ResponsibilityAssignment(models.Model):
    """
    Model representing an assignment of a responsibility to a user.
    """
    user: Any = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='responsibility_assignments'
    )
    responsibility: Any = models.ForeignKey(
        Responsibility,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    obligation: Any = models.ForeignKey(
        'obligations.Obligation',
        on_delete=models.CASCADE,
        related_name='responsibility_assignments'
    )
    role: Any = models.ForeignKey(
        Responsibility,
        on_delete=models.CASCADE,
        related_name='role_assignments'
    )
    created_by: Any = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_responsibility_assignments'
    )
    created_at: Any = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Responsibility Assignment'
        verbose_name_plural = 'Responsibility Assignments'
        ordering = ['-created_at']
        unique_together = ['user', 'obligation', 'role']

    def __str__(self) -> str:
        return f"{self.user} - {self.role} for {self.obligation}"
