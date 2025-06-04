from beartype import beartype
from django.db import models


@beartype
class AuthUser(models.Model):
    """Authentication user model.

    Attributes:
        id (int): The primary key for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The hashed password of the user.

    """

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    # Example usage for role field (if/when added):
    # role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default=ROLE_USER)

    def __str__(self) -> str:
        """Return a string representation of the user."""
        return self.username

    class Meta:
        permissions = [
            ("view_authuser", "Can view auth user"),
            ("change_authuser", "Can change auth user"),
            ("delete_authuser", "Can delete auth user"),
        ]
        default_permissions = ("add", "change", "delete", "view")
        # Enable object-level permissions for django-guardian
