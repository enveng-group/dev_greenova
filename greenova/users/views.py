from typing import TYPE_CHECKING, Any

from django.contrib import messages
from django.contrib.auth import (
    get_user_model,  # Updated import for User model
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from beartype import beartype

from .forms import AdminUserForm, ProfileImageForm, UserProfileForm
from .serializers import (
    UserProtoSerializer,
    UserCollectionProtoSerializer,
)

if TYPE_CHECKING:
    from .models import Profile

User = get_user_model()  # Use the recommended method to get the User model


@beartype
def is_admin(user) -> bool:
    """Check if the user is an admin."""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@beartype
@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """View for displaying user's profile."""
    profile: Profile = request.user.profile
    context: dict[str, Any] = {
        "profile": profile,
    }

    return render(request, "users/profile_detail.html", context)


@beartype
@login_required
def profile_edit(request: HttpRequest) -> HttpResponse:
    """View for editing user's profile."""
    profile: Profile = request.user.profile

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
    """View for changing user password."""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update session to prevent logout
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
    """View for uploading a profile image."""
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

    context = {
        "form": form,
    }

    return render(request, "users/profile_image_form.html", context)


@beartype
@user_passes_test(is_admin)
def admin_user_list(request: HttpRequest) -> HttpResponse:
    """View for displaying all users to an admin."""
    users = User.objects.all().select_related("profile").order_by("-is_staff", "username")

    context = {
        "users": users,
    }

    return render(request, "users/admin_user_list.html", context)


@beartype
@user_passes_test(is_admin)
def admin_user_create(request: HttpRequest) -> HttpResponse:
    """Admin view for creating new users."""
    if request.method == "POST":
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User {user.username} created successfully.")
            return redirect("users:admin_user_list")
    else:
        form = AdminUserForm()

    context = {
        "form": form,
        "action": "Create",
    }

    return render(request, "users/admin_user_form.html", context)


@beartype
@user_passes_test(is_admin)
def admin_user_edit(request: HttpRequest, user_id: int) -> HttpResponse:
    """Admin view for editing users."""
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

    context = {
        "form": form,
        "profile_form": profile_form,
        "user_obj": user_obj,
        "action": "Edit",
    }

    return render(request, "users/admin_user_form.html", context)


@beartype
@user_passes_test(is_admin)
def admin_user_delete(request: HttpRequest, user_id: int) -> HttpResponse:
    """Admin view for deleting users."""
    user_obj = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        username = user_obj.username
        user_obj.delete()
        messages.success(request, f"User {username} deleted successfully.")
        return redirect("users:admin_user_list")

    context = {
        "user_obj": user_obj,
    }

    return render(request, "users/admin_user_delete.html", context)


@beartype
@login_required
def export_user(request, user_id: int) -> HttpResponse:
    """Export a single user as Protocol Buffer binary data."""
    if request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)
    else:
        user = get_object_or_404(User, id=user_id, id=request.user.id)
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
def export_all_users(request) -> HttpResponse:
    """Export all users as a Protocol Buffer collection."""
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
def import_user(request) -> HttpResponse:
    """Import a user from Protocol Buffer binary data."""
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
