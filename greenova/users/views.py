from typing import Any

from company.models import CompanyMembership
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django_htmx.http import trigger_client_event
from obligations.models import Obligation
from projects.models import Project

from .forms import AdminUserForm, ProfileImageForm, UserProfileForm
from .models import Profile

User = get_user_model()


def is_admin(user: User) -> bool:
    """Check if the user is an admin."""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """View for displaying user's profile."""
    profile: Profile = request.user.profile

    company_memberships = CompanyMembership.objects.filter(user_id=request.user.id)

    if not company_memberships:
        context: dict[str, Any] = {"profile": profile, "overdue_count": 0}
    else:
        # Get all the roles this user has across companies
        user_roles = company_memberships.values_list("role", flat=True).distinct()

        # Find obligations that match any of the user's roles
        project_ids = Project.objects.filter(members=request.user.id).values_list(
            "id", flat=True
        )

        # Find obligations that match any of the user's roles and are in their projects
        obligations = (
            Obligation.objects.filter(
                responsibility__in=user_roles, project_id__in=project_ids
            )
            .select_related("project")
            .distinct()
        )

        # Get obligations that are overdue
        overdue_obligations = [
            obligation for obligation in obligations if obligation.is_overdue
        ]

        context: dict[str, Any] = {
            "profile": profile,
            "overdue_count": len(overdue_obligations),
        }

    if request.htmx:
        return render(request, "users/partials/profile_detail.html", context)
    return render(request, "users/profile_detail.html", context)


@login_required
def profile_edit(request):
    """View for editing user's profile."""
    profile = request.user.profile

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")

            if request.htmx:
                response = render(
                    request, "users/partials/profile_detail.html", {"profile": profile}
                )
                return trigger_client_event(response, "profileUpdated", {})
            return redirect("users:profile")

        messages.error(request, "Please correct the errors below.")
    else:
        # Initialize form with current user data
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
def change_password(request):
    """View for changing password."""
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")

            if request.htmx:
                return HttpResponse(
                    '<div class="alert success">Password changed successfully.</div>',
                    headers={"HX-Trigger": "passwordChanged"},
                )
            return redirect("users:profile")
    else:
        form = PasswordChangeForm(request.user)

    context = {"form": form}

    if request.htmx:
        return render(request, "users/partials/password_change_form.html", context)
    return render(request, "users/password_change.html", context)


@login_required
@require_http_methods(["POST"])
def upload_profile_image(request):
    """AJAX view for uploading profile image."""
    form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
    if form.is_valid():
        form.save()
        return JsonResponse(
            {"status": "success", "image_url": request.user.profile.profile_image.url}
        )
    return JsonResponse({"status": "error", "errors": form.errors})


@user_passes_test(is_admin)
def admin_user_list(request):
    """Admin view for listing all users."""
    users = User.objects.all().order_by("-date_joined")

    context = {"users": users}

    if request.htmx:
        return render(request, "users/partials/admin_user_list.html", context)
    return render(request, "users/admin_user_list.html", context)


@user_passes_test(is_admin)
def admin_user_create(request):
    """Admin view for creating a new user."""
    if request.method == "POST":
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User {user.username} created successfully!")

            if request.htmx:
                return HttpResponse(
                    '<div class="alert success">User created successfully.</div>',
                    headers={"HX-Redirect": reverse("users:admin_user_list")},
                )
            return redirect("users:admin_user_list")
    else:
        form = AdminUserForm()

    context = {"form": form, "action": "Create"}

    if request.htmx:
        return render(request, "users/partials/admin_user_form.html", context)
    return render(request, "users/admin_user_form.html", context)


@user_passes_test(is_admin)
def admin_user_edit(request, user_id):
    """Admin view for editing a user."""
    user_obj = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = AdminUserForm(request.POST, instance=user_obj)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_obj.profile
        )

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, f"User {user_obj.username} updated successfully!")

            if request.htmx:
                return HttpResponse(
                    '<div class="alert success">User updated successfully.</div>',
                    headers={"HX-Redirect": reverse("users:admin_user_list")},
                )
            return redirect("users:admin_user_list")
    else:
        form = AdminUserForm(instance=user_obj)
        profile_form = UserProfileForm(instance=user_obj.profile)

    context = {
        "form": form,
        "profile_form": profile_form,
        "user_obj": user_obj,
        "action": "Update",
    }

    if request.htmx:
        return render(request, "users/partials/admin_user_form.html", context)
    return render(request, "users/admin_user_form.html", context)


@user_passes_test(is_admin)
def admin_user_delete(request, user_id):
    """Admin view for deleting a user."""
    user_obj = get_object_or_404(User, id=user_id)

    # Prevent admins from deleting themselves
    if user_obj == request.user:
        messages.error(request, "You cannot delete your own account!")
        return redirect("users:admin_user_list")

    if request.method == "POST":
        username = user_obj.username
        user_obj.delete()
        messages.success(request, f"User {username} deleted successfully!")

        if request.htmx:
            users = User.objects.all().order_by("-date_joined")
            html = render_to_string(
                "users/partials/admin_user_list.html", {"users": users}
            )
            return HttpResponse(html)
        return redirect("users:admin_user_list")

    context = {"user_obj": user_obj}

    if request.htmx:
        return render(request, "users/partials/admin_user_delete_confirm.html", context)
    return render(request, "users/admin_user_delete.html", context)
