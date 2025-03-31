<<<<<<< HEAD
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
=======
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string

from .models import Profile
from .forms import UserProfileForm, AdminUserForm, ProfileImageForm


def is_admin(user):
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
    """Check if the user is an admin."""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
<<<<<<< HEAD
def profile_view(request: HttpRequest) -> HttpResponse:
    """View for displaying user's profile."""
    profile: Profile = request.user.profile
    context: Dict[str, Any] = {
=======
def profile_view(request):
    """View for displaying user's profile."""
    profile = request.user.profile
    context = {
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
        'profile': profile,
    }

    if request.htmx:
        return render(request, 'users/partials/profile_detail.html', context)
    return render(request, 'users/profile_detail.html', context)


@login_required
<<<<<<< HEAD
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
=======
def profile_edit(request):
    """View for editing user's profile."""
    profile = request.user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")

            # If this is an HTMX request, return just the updated profile detail
            if request.htmx:
                response = render(request, 'users/partials/profile_detail.html', {
                    'profile': profile,
                })
                return trigger_client_event(response, 'profileUpdated', {})

            return redirect('users:profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Initialize form with current user data
        form = UserProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    context = {
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
        'form': form,
        'profile': profile,
    }

    if request.htmx:
<<<<<<< HEAD
        return render(request, 'users/partials/profile_edit.html', context)
=======
        return render(request, 'users/partials/profile_edit_form.html', context)
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
    return render(request, 'users/profile_edit.html', context)


@login_required
<<<<<<< HEAD
def change_password(request: HttpRequest) -> HttpResponse:
    """View for changing user password."""
=======
def change_password(request):
    """View for changing password."""
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
<<<<<<< HEAD
            # Update session to prevent logout
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
=======
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')

            if request.htmx:
                return HttpResponse(
                    '<div class="alert success">Password changed successfully.</div>',
                    headers={'HX-Trigger': 'passwordChanged'}
                )
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
            return redirect('users:profile')
    else:
        form = PasswordChangeForm(request.user)

<<<<<<< HEAD
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

=======
    context = {'form': form}

    if request.htmx:
        return render(request, 'users/partials/password_change_form.html', context)
    return render(request, 'users/password_change.html', context)


@login_required
@require_http_methods(["POST"])
def upload_profile_image(request):
    """AJAX view for uploading profile image."""
    form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'status': 'success',
            'image_url': request.user.profile.profile_image.url
        })
    return JsonResponse({'status': 'error', 'errors': form.errors})


@user_passes_test(is_admin)
def admin_user_list(request):
    """Admin view for listing all users."""
    users = User.objects.all().order_by('-date_joined')

    context = {'users': users}

    if request.htmx:
        return render(request, 'users/partials/admin_user_list.html', context)
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
    return render(request, 'users/admin_user_list.html', context)


@user_passes_test(is_admin)
<<<<<<< HEAD
def admin_user_create(request: HttpRequest) -> HttpResponse:
    """Admin view for creating new users."""
=======
def admin_user_create(request):
    """Admin view for creating a new user."""
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save()
<<<<<<< HEAD
            messages.success(request, f'User {user.username} created successfully.')
=======
            messages.success(request, f"User {user.username} created successfully!")

            if request.htmx:
                return HttpResponse(
                    '<div class="alert success">User created successfully.</div>',
                    headers={'HX-Redirect': reverse('users:admin_user_list')}
                )
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
            return redirect('users:admin_user_list')
    else:
        form = AdminUserForm()

<<<<<<< HEAD
    context = {
        'form': form,
        'action': 'Create',
    }

=======
    context = {'form': form, 'action': 'Create'}

    if request.htmx:
        return render(request, 'users/partials/admin_user_form.html', context)
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
    return render(request, 'users/admin_user_form.html', context)


@user_passes_test(is_admin)
<<<<<<< HEAD
def admin_user_edit(request: HttpRequest, user_id: int) -> HttpResponse:
    """Admin view for editing users."""
=======
def admin_user_edit(request, user_id):
    """Admin view for editing a user."""
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
    user_obj = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = AdminUserForm(request.POST, instance=user_obj)
<<<<<<< HEAD
        profile_form = UserProfileForm(request.POST, instance=user_obj.profile)
=======
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_obj.profile)
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
<<<<<<< HEAD
            messages.success(request, f'User {user_obj.username} updated successfully.')
=======
            messages.success(request, f"User {user_obj.username} updated successfully!")

            if request.htmx:
                return HttpResponse(
                    '<div class="alert success">User updated successfully.</div>',
                    headers={'HX-Redirect': reverse('users:admin_user_list')}
                )
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
            return redirect('users:admin_user_list')
    else:
        form = AdminUserForm(instance=user_obj)
        profile_form = UserProfileForm(instance=user_obj.profile)

    context = {
        'form': form,
        'profile_form': profile_form,
        'user_obj': user_obj,
<<<<<<< HEAD
        'action': 'Edit',
    }

=======
        'action': 'Update'
    }

    if request.htmx:
        return render(request, 'users/partials/admin_user_form.html', context)
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
    return render(request, 'users/admin_user_form.html', context)


@user_passes_test(is_admin)
<<<<<<< HEAD
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
=======
def admin_user_delete(request, user_id):
    """Admin view for deleting a user."""
    user_obj = get_object_or_404(User, id=user_id)

    # Prevent admins from deleting themselves
    if user_obj == request.user:
        messages.error(request, "You cannot delete your own account!")
        return redirect('users:admin_user_list')

    if request.method == 'POST':
        username = user_obj.username
        user_obj.delete()
        messages.success(request, f"User {username} deleted successfully!")

        if request.htmx:
            users = User.objects.all().order_by('-date_joined')
            html = render_to_string('users/partials/admin_user_list.html', {'users': users})
            return HttpResponse(html)
        return redirect('users:admin_user_list')

    context = {'user_obj': user_obj}
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

    if request.htmx:
        return render(request, 'users/partials/admin_user_delete_confirm.html', context)
    return render(request, 'users/admin_user_delete.html', context)
