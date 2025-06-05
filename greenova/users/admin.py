"""Admin configuration for the users app.

This module customizes the Django admin interface for user and profile models.
It includes runtime type checking with beartype and Google style docstrings.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any, Optional

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Profile
from .permissions import user_can_view_user
from beartype import beartype


class ProfileInline(admin.StackedInline):
    """Inline admin for user profiles."""

    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"

    @beartype
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the ProfileInline admin.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

    @beartype
    def has_add_permission(self, request: Any) -> bool:
        """Determine if the user has permission to add a profile.

        Args:
            request: The HTTP request object.

        Returns:
            True if the user has permission, False otherwise.
        """
        return super().has_add_permission(request)

    @beartype
    def has_change_permission(self, request: Any, obj: Optional[Any] = None) -> bool:
        """Determine if the user has permission to change a profile.

        Args:
            request: The HTTP request object.
            obj: The profile object (optional).

        Returns:
            True if the user has permission, False otherwise.
        """
        return super().has_change_permission(request, obj=obj)

    @beartype
    def has_delete_permission(self, request: Any, obj: Optional[Any] = None) -> bool:
        """Determine if the user has permission to delete a profile.

        Args:
            request: The HTTP request object.
            obj: The profile object (optional).

        Returns:
            True if the user has permission, False otherwise.
        """
        return super().has_delete_permission(request, obj=obj)


class UserAdmin(BaseUserAdmin):
    """Enhanced User admin with Profile inline."""

    inlines = (ProfileInline,)
    list_display = (
        "username", "email", "first_name", "last_name", "is_staff", "is_active",
    )

    @beartype
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the UserAdmin.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

    @beartype
    def has_add_permission(self, request: Any) -> bool:
        """Determine if the user has permission to add a user.

        Args:
            request: The HTTP request object.

        Returns:
            True if the user has permission, False otherwise.
        """
        return super().has_add_permission(request)

    @beartype
    def has_change_permission(
        self, request: Any, obj: Optional[Any] = None
    ) -> bool:
        """Determine if the user has permission to change a user.

        Args:
            request: The HTTP request object.
            obj: The user object (optional).

        Returns:
            True if the user has permission, False otherwise.
        """
        return super().has_change_permission(request, obj=obj)

    @beartype
    def has_delete_permission(
        self, request: Any, obj: Optional[Any] = None
    ) -> bool:
        """Determine if the user has permission to delete a user.

        Args:
            request: The HTTP request object.
            obj: The user object (optional).

        Returns:
            True if the user has permission, False otherwise.
        """
        return super().has_delete_permission(request, obj=obj)

    @beartype
    def save_model(
        self, request: Any, obj: Any, form: Any, change: bool
    ) -> None:
        """Save the user model instance.

        Args:
            request: The HTTP request object.
            obj: The user object to save.
            form: The form instance.
            change: Whether this is a change to an existing object.

        Returns:
            None
        """
        super().save_model(request, obj, form, change)

    @beartype
    def get_queryset(self, request: Any) -> Any:
        """Get the queryset for the admin list view.

        Args:
            request: The HTTP request object.

        Returns:
            The queryset of users.
        """
        return super().get_queryset(request)

    @beartype
    def get_inline_instances(self, request: Any, obj: Optional[Any] = None) -> list[Any]:
        """Get the inline instances for the admin.

        Args:
            request: The HTTP request object.
            obj: The user object (optional).

        Returns:
            A list of inline instances.
        """
        return super().get_inline_instances(request, obj=obj)


# Unregister the default User admin and register our enhanced version
admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
