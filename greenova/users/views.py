from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth import get_user_model  # Updated import for User model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AdminUserForm, ProfileImageForm, UserProfileForm
from .models import Profile

User = get_user_model()  # Use the recommended method to get the User model


def is_admin(user: User) -> bool:
    """Check if the user is an admin."""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """View for displaying user's profile."""
    profile: Profile = request.user.profile
    context: Dict[str, Any] = {
        "profile": profile,
    }

    if request.htmx:
        return render(request, "users/partials/profile_detail.html", context)
    return render(request, "users/profile_detail.html", context)


@login_required
def profile_edit(request: HttpRequest) -> HttpResponse:
    """View for editing user's profile."""
    profile: Profile = request.user.profile

    if request.method == "POST":
        form = UserProfileForm(
            request.POST,
            instance=profile,
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            },
        )
        if form.is_valid():
            # Save profile data
            updated_profile = form.save(commit=False)
            updated_profile.save()

            # Update user data
            user = request.user
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.save()

            messages.success(request, "Profile updated successfully.")

            if request.htmx:
                return profile_view(request)
            return redirect("users:profile")
    else:
        form = UserProfileForm(
            instance=profile,
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
            },
        )

    context = {
        "form": form,
        "profile": profile,
    }

    if request.htmx:
        return render(request, "users/partials/profile_edit_form.html", context)
    return render(request, "users/profile_edit.html", context)


@login_required
def change_password(request: HttpRequest) -> HttpResponse:
    """View for changing user password."""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")

            if request.htmx:
                return profile_view(request)
            return redirect("users:profile")
    else:
        form = PasswordChangeForm(request.user)

    context = {
        "form": form,
    }

    if request.htmx:
        return render(request, "users/partials/password_change_form.html", context)
    return render(request, "users/password_change.html", context)


@login_required
def upload_profile_image(request: HttpRequest) -> HttpResponse:
    """View for uploading a profile image."""
    if request.method == "POST":
        form = ProfileImageForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile image updated successfully.")

            if request.htmx:
                return JsonResponse(
                    {
                        "success": True,
                        "image_url": request.user.profile.profile_image.url,
                    }
                )
            return redirect("users:profile")
    else:
        form = ProfileImageForm(instance=request.user.profile)

    context = {
        "form": form,
    }

    return render(request, "users/partials/profile_image_form.html", context)


@user_passes_test(is_admin)
def admin_user_list(request: HttpRequest) -> HttpResponse:
    """Admin view for listing users."""
    users = User.objects.all().order_by("-date_joined")

    context = {
        "users": users,
    }

    if request.htmx:
        return render(request, "users/partials/admin_user_list.html", context)
    return render(request, "users/admin_user_list.html", context)


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

    if request.htmx:
        return render(request, "users/partials/admin_user_delete_confirm.html", context)
    return render(request, "users/admin_user_delete.html", context)
