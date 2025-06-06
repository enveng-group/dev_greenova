# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Views for user profile, admin user management, and protobuf import/export.

This module provides Django views for user profile display and editing,
admin user CRUD, password changes, profile image uploads, and import/export
of users using Protocol Buffer serialization.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Views for user profile, admin user management, and protobuf import/export

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from typing import TYPE_CHECKING, Any

from django.contrib import messages
from django.contrib.auth import (
    get_user_model,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from beartype import beartype

from .forms import AdminUserForm, ProfileImageForm, UserProfileForm
from .serializers import (
    UserProtoSerializer,
    UserCollectionProtoSerializer,
)
from .permissions import user_can_view_user
from .types import (
    UserProfileDict,
    UserPermissionsDict,
    SessionDataDict,
    UserProfileManager,
    PermissionManager,
    UserSessionManager,
)

if TYPE_CHECKING:
    from .models import Profile

User = get_user_model()

# --- Profile Completion View ---
@beartype
@login_required
@require_http_methods(["GET", "POST"])
def profile_complete(request: HttpRequest) -> HttpResponse:
    """View for completing user profile if incomplete.

    Args:
        request: The HTTP request.

    Returns:
        Rendered profile completion form or redirect after completion.
    """
    profile = request.user.profile
    if getattr(profile, "has_completed_profile", False):
        return redirect("users:profile")
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Mark profile as complete
            setattr(profile, "has_completed_profile", True)
            profile.save()
            messages.success(request, "Profile completed successfully.")
            return redirect("users:profile")
    else:
        form = UserProfileForm(instance=profile)
    context: dict[str, Any] = {
        "form": form,
        "profile": profile,
        "page_title": "Complete Your Profile",
    }
    return render(request, "users/profile_complete.html", context)

@beartype
def is_admin(user: Any) -> bool:
    """Check if the user is an admin.

    Args:
        user: The user object.

    Returns:
        True if user is staff or superuser, False otherwise.
    """
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@beartype
@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """View for displaying user's profile.

    Args:
        request: The HTTP request.

    Returns:
        Rendered profile detail page.
    """
    profile: "Profile" = request.user.profile
    context: dict[str, Any] = {
        "profile": profile,
    }
    return render(request, "users/profile_detail.html", context)


@beartype
@login_required
def profile_edit(request: HttpRequest) -> HttpResponse:
    """View for editing user's profile.

    Args:
        request: The HTTP request.

    Returns:
        Rendered profile edit page or redirect after save.
    """
    profile: "Profile" = request.user.profile

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("users:profile")
    else:
        form = UserProfileForm(instance=profile)

    context: dict[str, Any] = {
        "form": form,
        "profile": profile,
    }

    return render(request, "users/profile_edit.html", context)


@beartype
@login_required
def change_password(request: HttpRequest) -> HttpResponse:
    """View for changing user password.

    Args:
        request: The HTTP request.

    Returns:
        Rendered password change page or redirect after save.
    """
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("users:profile")
    else:
        form = PasswordChangeForm(request.user)

    context: dict[str, Any] = {"form": form}

    return render(request, "users/change_password.html", context)


@beartype
@login_required
def upload_profile_image(request: HttpRequest) -> HttpResponse:
    """View for uploading a profile image.

    Args:
        request: The HTTP request.

    Returns:
        Rendered profile image upload form or redirect after save.
    """
    if request.method == "POST":
        form = ProfileImageForm(
            request.POST, request.FILES, instance=request.user.profile,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile image updated successfully.")
            return redirect("users:profile")
    else:
        form = ProfileImageForm(instance=request.user.profile)

    context: dict[str, Any] = {
        "form": form,
    }

    return render(request, "users/profile_image_form.html", context)


@beartype
@user_passes_test(is_admin)
def admin_user_list(request: HttpRequest) -> HttpResponse:
    """View for displaying all users to an admin.

    Args:
        request: The HTTP request.

    Returns:
        Rendered admin user list page.
    """
    users = User.objects.all().select_related("profile").order_by("-is_staff", "username")

    context: dict[str, Any] = {
        "users": users,
    }

    return render(request, "users/admin_user_list.html", context)


@beartype
@user_passes_test(is_admin)
def admin_user_create(request: HttpRequest) -> HttpResponse:
    """Admin view for creating new users.

    Args:
        request: The HTTP request.

    Returns:
        Rendered admin user creation form or redirect after save.
    """
    if request.method == "POST":
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User {user.username} created successfully.")
            return redirect("users:admin_user_list")
    else:
        form = AdminUserForm()

    context: dict[str, Any] = {
        "form": form,
        "action": "Create",
    }

    return render(request, "users/admin_user_form.html", context)


@beartype
@user_passes_test(is_admin)
def admin_user_edit(request: HttpRequest, user_id: int) -> HttpResponse:
    """Admin view for editing users.

    Args:
        request: The HTTP request.
        user_id: The ID of the user to edit.

    Returns:
        Rendered admin user edit form or redirect after save.
    """
    user_obj = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = AdminUserForm(request.POST, instance=user_obj)
        profile_form = UserProfileForm(request.POST, instance=user_obj.profile)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, f"User {user_obj.username} updated successfully.")
            return redirect("users:admin_user_list")
    else:
        form = AdminUserForm(instance=user_obj)
        profile_form = UserProfileForm(instance=user_obj.profile)

    context: dict[str, Any] = {
        "form": form,
        "profile_form": profile_form,
        "user_obj": user_obj,
        "action": "Edit",
    }

    return render(request, "users/admin_user_form.html", context)


@beartype
@user_passes_test(is_admin)
def admin_user_delete(request: HttpRequest, user_id: int) -> HttpResponse:
    """Admin view for deleting users.

    Args:
        request: The HTTP request.
        user_id: The ID of the user to delete.

    Returns:
        Rendered admin user delete confirmation or redirect after delete.
    """
    user_obj = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        username = user_obj.username
        user_obj.delete()
        messages.success(request, f"User {username} deleted successfully.")
        return redirect("users:admin_user_list")

    context: dict[str, Any] = {
        "user_obj": user_obj,
    }

    return render(request, "users/admin_user_delete.html", context)


@beartype
@login_required
def export_user(request: HttpRequest, user_id: int) -> HttpResponse:
    """Export a single user as Protocol Buffer binary data.

    Args:
        request: The HTTP request.
        user_id: The ID of the user to export.

    Returns:
        HTTP response with protobuf binary data or redirect on error.
    """
    if not user_can_view_user(request.user, user_id):
        messages.error(request, "You do not have permission to export this user.")
        return redirect("users:profile")
    user = get_object_or_404(User, id=user_id)
    serializer = UserProtoSerializer(instance=user)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export user.")
        return redirect("users:profile")
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = f'attachment; filename="user_{user_id}.pb"'
    return response


@beartype
@login_required
def export_all_users(request: HttpRequest) -> HttpResponse:
    """Export all users as a Protocol Buffer collection.

    Args:
        request: The HTTP request.

    Returns:
        HTTP response with protobuf binary data or redirect on error.
    """
    if request.user.is_superuser:
        users = list(User.objects.all())
    else:
        users = [request.user]
    serializer = UserCollectionProtoSerializer(instances=users)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export users.")
        return redirect("users:profile")
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="users.pb"'
    return response


@beartype
@login_required
@require_http_methods(["GET", "POST"])
def import_user(request: HttpRequest) -> HttpResponse:
    """Import a user from Protocol Buffer binary data.

    Args:
        request: The HTTP request.

    Returns:
        Rendered import form or redirect after import.
    """
    if request.method == "POST":
        if "file" not in request.FILES:
            messages.error(request, "No file was provided.")
            return redirect("users:import_user")
        uploaded_file = request.FILES["file"]
        try:
            data = uploaded_file.read()
            serializer = UserProtoSerializer(data=data)
            if not serializer.is_valid():
                messages.error(
                    request, "Could not deserialize the file. Invalid format.")
                return redirect("users:import_user")
            user = serializer.validated_data
            user.id = None  # Ensure a new record is created
            user.save()
            messages.success(request, "User imported successfully.")
            return redirect("users:profile")
        except (ValueError, OSError, AttributeError, TypeError):
            messages.error(request, "An error occurred while importing the user.")
            return redirect("users:import_user")
    # GET request - show import form
    return render(request, "users/import_user.html", {
        "page_title": "Import User",
    })


class UserListView(LoginRequiredMixin, ListView):
    """List view for all users."""
    model = User
    template_name = "users/users_list.html"
    context_object_name = "users"

    def get_queryset(self):
        """Return all users ordered by username."""
        return User.objects.all().order_by("username")
