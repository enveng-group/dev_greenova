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
        'profile': profile,
    }

    if request.htmx:
        return render(request, 'users/partials/profile_detail.html', context)
    return render(request, 'users/profile_detail.html', context)


@login_required
def profile_edit(request: HttpRequest) -> HttpResponse:
    """View for editing user's profile."""
    profile: Profile = request.user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=profile)

    context: Dict[str, Any] = {
        'form': form,
        'profile': profile,
    }

    if request.htmx:
        return render(request, 'users/partials/profile_edit.html', context)
    return render(request, 'users/profile_edit.html', context)


@login_required
def change_password(request: HttpRequest) -> HttpResponse:
    """View for changing user password."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update session to prevent logout
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:profile')
    else:
        form = PasswordChangeForm(request.user)

    context: Dict[str, Any] = {'form': form}

    if request.htmx:
        return render(request, 'users/partials/change_password.html', context)
    return render(request, 'users/change_password.html', context)


@login_required
def upload_profile_image(request: HttpRequest) -> HttpResponse:
    """View for uploading a profile image."""
    if request.method == 'POST':
        form = ProfileImageForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile image updated successfully.')

            if request.htmx:
                return JsonResponse(
                    {
                        'success': True,
                        'image_url': request.user.profile.profile_image.url,
                    }
                )
            return redirect('users:profile')
    else:
        form = ProfileImageForm(instance=request.user.profile)

    context = {
        'form': form,
    }

    return render(request, 'users/partials/profile_image_form.html', context)


@user_passes_test(is_admin)
def admin_user_list(request: HttpRequest) -> HttpResponse:
    """View for displaying all users to an admin."""
    users = User.objects.all().select_related('profile').order_by('-is_staff', 'username')

    context = {
        'users': users,
    }

    return render(request, 'users/admin_user_list.html', context)


@user_passes_test(is_admin)
def admin_user_create(request: HttpRequest) -> HttpResponse:
    """Admin view for creating new users."""
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully.')
            return redirect('users:admin_user_list')
    else:
        form = AdminUserForm()

    context = {
        'form': form,
        'action': 'Create',
    }

    return render(request, 'users/admin_user_form.html', context)


@user_passes_test(is_admin)
def admin_user_edit(request: HttpRequest, user_id: int) -> HttpResponse:
    """Admin view for editing users."""
    user_obj = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = AdminUserForm(request.POST, instance=user_obj)
        profile_form = UserProfileForm(request.POST, instance=user_obj.profile)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, f'User {user_obj.username} updated successfully.')
            return redirect('users:admin_user_list')
    else:
        form = AdminUserForm(instance=user_obj)
        profile_form = UserProfileForm(instance=user_obj.profile)

    context = {
        'form': form,
        'profile_form': profile_form,
        'user_obj': user_obj,
        'action': 'Edit',
    }

    return render(request, 'users/admin_user_form.html', context)


@user_passes_test(is_admin)
def admin_user_delete(request: HttpRequest, user_id: int) -> HttpResponse:
    """Admin view for deleting users."""
    user_obj = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        username = user_obj.username
        user_obj.delete()
        messages.success(request, f'User {username} deleted successfully.')
        return redirect('users:admin_user_list')

    context = {
        'user_obj': user_obj,
    }

    if request.htmx:
        return render(request, 'users/partials/admin_user_delete_confirm.html', context)
    return render(request, 'users/admin_user_delete.html', context)
