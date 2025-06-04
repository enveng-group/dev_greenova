from beartype import beartype
from django.db import models


@beartype
class AppSetting(models.Model):
    """Stub model for application settings.

    Attributes:
        id (int): The primary key for the setting.
        name (str): The name of the setting.
        value (str): The value of the setting.

    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        permissions = [
            ("view_appsetting", "Can view app setting"),
            ("change_appsetting", "Can change app setting"),
            ("delete_appsetting", "Can delete app setting"),
        ]
        default_permissions = ("add", "change", "delete", "view")
        # Enable object-level permissions for django-guardian

    def __str__(self) -> str:
        """Return a string representation of the setting."""
        return f"{self.name}: {self.value}"
