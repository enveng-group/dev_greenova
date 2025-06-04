from core.utils.roles import get_responsibility_choices
from django.conf import settings
from django.db import models
from django.db.models import CharField, TextField
from obligations.models import Obligation


class Responsibility(models.Model):
    """Model representing a responsibility that can be assigned to obligations.
    These values match the responsibility choices in obligations.models.Obligation.
    """

    name: CharField = models.CharField(
        max_length=255,
        unique=True,
        choices=get_responsibility_choices(),
    )
    description: TextField | None = models.TextField(blank=True)

    class Meta:
        verbose_name = "Responsibility"
        verbose_name_plural = "Responsibilities"
        ordering = ["name"]

    def __str__(self) -> str:
        return str(self.name)


class ResponsibilityAssignment(models.Model):
    """Assignment of a user to an obligation/task with a responsibility role."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="responsibility_assignments",
    )
    obligation = models.ForeignKey(
        Obligation,
        on_delete=models.CASCADE,
        related_name="responsibility_assignments",
    )
    responsibility = models.ForeignKey(
        Responsibility,
        on_delete=models.PROTECT,
        related_name="assignments",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "obligation", "responsibility")
        verbose_name = "Responsibility Assignment"
        verbose_name_plural = "Responsibility Assignments"
        ordering = ["obligation", "user", "responsibility"]

    def __str__(self) -> str:
        return f"{self.user} - {self.obligation} ({self.responsibility})"
