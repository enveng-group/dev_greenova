from beartype import beartype
from core.utils.roles import get_responsibility_choices
from django.conf import settings
from django.db import models
from django.db.models import CharField, TextField


@beartype
class Responsibility(models.Model):
    """Model representing a responsibility that can be assigned to obligations.

    These values match the responsibility choices in obligations.models.Obligation.

    Attributes:
        name (CharField): The name of the responsibility.
        description (TextField | None): A description of the responsibility.

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
        permissions = [
            ("view_responsibility", "Can view responsibility"),
            ("change_responsibility", "Can change responsibility"),
            ("delete_responsibility", "Can delete responsibility"),
        ]
        default_permissions = ("add", "change", "delete", "view")
        # Enable object-level permissions for django-guardian

    def __str__(self) -> str:
        return str(self.name)


@beartype
class ResponsibilityAssignment(models.Model):
    """Assignment of a user to an obligation/task with a responsibility role.

    Attributes:
        user (ForeignKey): The user assigned to the responsibility.
        obligation (ForeignKey): The obligation/task associated with the responsibility.
        responsibility (ForeignKey): The responsibility role assigned.
        assigned_at (DateTimeField): The timestamp when the assignment was created.
        updated_at (DateTimeField): The timestamp when the assignment was last updated.

    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="responsibility_assignments",
    )
    obligation = models.ForeignKey(
        "obligations.Obligation",  # Use string reference to avoid circular import
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
        permissions = [
            ("view_responsibilityassignment", "Can view responsibility assignment"),
            ("change_responsibilityassignment", "Can change responsibility assignment"),
            ("delete_responsibilityassignment", "Can delete responsibility assignment"),
        ]
        default_permissions = ("add", "change", "delete", "view")
        # Enable object-level permissions for django-guardian

    def __str__(self) -> str:
        return f"{self.user} - {self.obligation} ({self.responsibility})"
