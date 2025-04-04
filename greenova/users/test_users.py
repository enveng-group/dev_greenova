import os
import sys
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, override_settings
from django.urls import reverse
from PIL import Image
from users.forms import AdminUserForm, ProfileImageForm, UserProfileForm
from users.models import Profile
from users.templatetags.user_tags import (auth_status_badge, auth_user_display,
                                          full_name_or_username, has_verified_email,
                                          profile_image_url, user_role)

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# -------------------- FIXTURES --------------------

@pytest.fixture
def user():
    """Create and return a regular user."""
    test_username = os.environ.get('TEST_USERNAME', 'testuser')
    test_email = os.environ.get('TEST_EMAIL', 'testuser@example.com')
    test_password = os.environ.get('TEST_PASSWORD', 'password123')

    return get_user_model().objects.create_user(
        username=test_username,
        email=test_email,
        password=test_password,
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def admin_user():
    """Create and return an admin user."""
    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')

    return get_user_model().objects.create_superuser(
        username=admin_username,
        email=admin_email,
        password=admin_password
    )


@pytest.fixture
def staff_user():
    """Create and return a staff user."""
    staff_username = os.environ.get('STAFF_USERNAME', 'staff')
    staff_email = os.environ.get('STAFF_EMAIL', 'staff@example.com')
    staff_password = os.environ.get('STAFF_PASSWORD', 'staff123')

    return get_user_model().objects.create_user(
        username=staff_username,
        email=staff_email,
        password=staff_password,
        is_staff=True
    )


@pytest.fixture
def profile(user):
    """Return the profile for the test user."""
    # Profile is created via signals, so we just need to get it
    return user.profile


@pytest.fixture
def profile_form_data():
    """Return valid data for the UserProfileForm."""
    return {
        'first_name': 'Updated',
        'last_name': 'Name',
        'email': 'updated@example.com',
        'bio': 'This is my updated bio',
        'position': 'Developer',
        'department': 'IT',
        'phone_number': '555-123-4567'
    }


@pytest.fixture
def admin_user_form_data():
    """Return valid data for the AdminUserForm."""
    return {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'first_name': 'New',
        'last_name': 'User',
        'password1': 'securepass123',
        'password2': 'securepass123',
        'is_active': True,
        'is_staff': False,
        'is_superuser': False
    }


@pytest.fixture
def rf():
    """Return a RequestFactory instance."""
    return RequestFactory()


@pytest.fixture
def mock_image():
    """Create a test image file."""
    file = BytesIO()
    image = Image.new('RGB', (100, 100), color='red')
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return SimpleUploadedFile(name='test.png', content=file.read(), content_type='image/png')


# -------------------- MODEL TESTS --------------------


@pytest.mark.django_db
class TestProfileModel:
    """Test the Profile model."""

    def test_profile_creation(self, user):
        """Test that a profile is automatically created with a user."""
        assert hasattr(user, 'profile')
        assert isinstance(user.profile, Profile)

    def test_profile_str(self, profile):
        """Test the string representation of a profile."""
        assert str(profile) == f"{profile.user.username}'s profile"

    def test_profile_fields(self, profile):
        """Test the fields of a profile."""
        profile.bio = 'This is my bio'
        profile.position = 'Developer'
        profile.department = 'IT'
        profile.phone_number = '555-123-4567'
        profile.save()

        refreshed_profile = Profile.objects.get(pk=profile.pk)
        assert refreshed_profile.bio == 'This is my bio'
        assert refreshed_profile.position == 'Developer'
        assert refreshed_profile.department == 'IT'
        assert refreshed_profile.phone_number == '555-123-4567'

    def test_profile_image_upload(self, profile, mock_image):
        """Test uploading a profile image."""
        profile.profile_image = mock_image
        profile.save()

        assert profile.profile_image
        assert 'test.png' in profile.profile_image.name

    def test_cascade_deletion(self):
        """Test that a profile is deleted when its user is deleted."""
        test_username = os.environ.get('TEST_USERNAME', 'temporary')
        test_email = os.environ.get('TEST_EMAIL', 'temp@example.com')
        test_password = os.environ.get('TEST_PASSWORD', 'temp123')

        user = get_user_model().objects.create_user(
            username=test_username,
            email=test_email,
            password=test_password
        )
        profile_id = user.profile.id
        user.delete()

        with pytest.raises(Profile.DoesNotExist):
            Profile.objects.get(pk=profile_id)


# -------------------- FORM TESTS --------------------


@pytest.mark.django_db
class TestUserProfileForm:
    """Test the UserProfileForm."""

    def test_valid_form(self, profile, profile_form_data):
        """Test that a valid form saves correctly."""
        form = UserProfileForm(data=profile_form_data, instance=profile)
        assert form.is_valid()

        updated_profile = form.save()
        assert updated_profile.user.first_name == 'Updated'
        assert updated_profile.user.last_name == 'Name'
        assert updated_profile.user.email == 'updated@example.com'
        assert updated_profile.bio == 'This is my updated bio'
        assert updated_profile.position == 'Developer'
        assert updated_profile.department == 'IT'
        assert updated_profile.phone_number == '555-123-4567'

    def test_init_populates_user_fields(self, profile):
        """Test that form initialization populates user fields."""
        profile.user.first_name = 'Initial'
        profile.user.last_name = 'User'
        profile.user.email = 'initial@example.com'
        profile.user.save()

        form = UserProfileForm(instance=profile)
        assert form.fields['first_name'].initial == 'Initial'
        assert form.fields['last_name'].initial == 'User'
        assert form.fields['email'].initial == 'initial@example.com'

    def test_invalid_email(self, profile):
        """Test that an invalid email is rejected."""
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalid-email',
            'bio': 'Test bio',
            'position': 'Developer',
            'department': 'IT',
            'phone_number': '555-123-4567'
        }
        form = UserProfileForm(data=form_data, instance=profile)
        assert not form.is_valid()
        assert 'email' in form.errors


@pytest.mark.django_db
class TestAdminUserForm:
    """Test the AdminUserForm."""

    def test_create_user(self, admin_user_form_data):
        """Test creating a new user."""
        form = AdminUserForm(data=admin_user_form_data)
        assert form.is_valid()

        user = form.save()
        assert user.username == 'newuser'
        assert user.email == 'newuser@example.com'
        assert user.first_name == 'New'
        assert user.last_name == 'User'
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        assert user.check_password('securepass123')

    def test_edit_user(self, user):
        """Test editing an existing user."""
        form_data = {
            'username': user.username,
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'is_active': True,
            'is_staff': True,
            'is_superuser': False,
        }
        form = AdminUserForm(data=form_data, instance=user)
        assert form.is_valid()

        updated_user = form.save()
        assert updated_user.email == 'updated@example.com'
        assert updated_user.first_name == 'Updated'
        assert updated_user.is_staff

    def test_password_mismatch(self):
        """Test that passwords that don't match are rejected."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password456',
            'is_active': True
        }
        form = AdminUserForm(data=form_data)
        assert not form.is_valid()
        assert 'password2' in form.errors

    def test_optional_password(self, user):
        """Test that password is optional when editing a user."""
        form_data = {
            'username': user.username,
            'email': user.email,
            'first_name': 'Updated',
            'last_name': 'Name',
            'is_active': True
        }
        form = AdminUserForm(data=form_data, instance=user)
        assert form.is_valid()


@pytest.mark.django_db
class TestProfileImageForm:
    """Test the ProfileImageForm."""

    def test_valid_image(self, profile, mock_image):
        """Test uploading a valid image."""
        form = ProfileImageForm(data={}, files={'profile_image': mock_image}, instance=profile)
        assert form.is_valid()

        updated_profile = form.save()
        assert updated_profile.profile_image
        assert 'test.png' in updated_profile.profile_image.name

    @override_settings(MEDIA_ROOT='/tmp/test-media/')
    def test_invalid_image(self, profile):
        """Test that an invalid image is rejected."""
        # Create an invalid image file
        invalid_image = SimpleUploadedFile(
            name='test.txt',
            content=b'not an image',
            content_type='text/plain'
        )
        form = ProfileImageForm(data={}, files={'profile_image': invalid_image}, instance=profile)
        assert not form.is_valid()


# -------------------- VIEW TESTS --------------------


@pytest.mark.django_db
class TestProfileViews:
    """Test the profile views."""

    def test_profile_view(self, client, user):
        """Test the profile view."""
        client.force_login(user)
        response = client.get(reverse('users:profile'))
        assert response.status_code == 200
        assert 'profile' in response.context
        assert response.context['profile'] == user.profile

    def test_profile_view_htmx(self, client, user):
        """Test the profile view with HTMX request."""
        client.force_login(user)
        response = client.get(
            reverse('users:profile'),
            HTTP_HX_REQUEST='true'
        )
        assert response.status_code == 200
        assert 'users/partials/profile_detail.html' in [t.name for t in response.templates]

    def test_profile_edit_get(self, client, user):
        """Test getting the profile edit form."""
        client.force_login(user)
        response = client.get(reverse('users:profile_edit'))
        assert response.status_code == 200
        assert 'form' in response.context
        assert isinstance(response.context['form'], UserProfileForm)

    def test_profile_edit_post(self, client, user, profile_form_data):
        """Test submitting the profile edit form."""
        client.force_login(user)
        response = client.post(reverse('users:profile_edit'), profile_form_data)
        assert response.status_code == 302
        assert response.url == reverse('users:profile')

        # Refresh user from database
        user.refresh_from_db()
        assert user.first_name == profile_form_data['first_name']
        assert user.profile.department == profile_form_data['department']

    def test_change_password_get(self, client, user):
        """Test getting the change password form."""
        client.force_login(user)
        response = client.get(reverse('users:change_password'))
        assert response.status_code == 200
        assert 'form' in response.context

    def test_change_password_post(self, client, user):
        """Test submitting the change password form."""
        client.force_login(user)
        password_data = {
            'old_password': 'password123',
            'new_password1': 'newpassword456',
            'new_password2': 'newpassword456'
        }
        response = client.post(reverse('users:change_password'), password_data)
        assert response.status_code == 302
        assert response.url == reverse('users:profile')

        # Verify password was changed
        user.refresh_from_db()
        assert user.check_password('newpassword456')

    def test_upload_profile_image(self, client, user, mock_image):
        """Test uploading a profile image."""
        client.force_login(user)
        response = client.post(
            reverse('users:upload_profile_image'),
            {'profile_image': mock_image}
        )
        assert response.status_code == 302
        assert response.url == reverse('users:profile')

        user.profile.refresh_from_db()
        assert user.profile.profile_image
        assert 'test.png' in user.profile.profile_image.name

    def test_upload_profile_image_htmx(self, client, user, mock_image):
        """Test uploading a profile image with HTMX request."""
        client.force_login(user)
        response = client.post(
            reverse('users:upload_profile_image'),
            {'profile_image': mock_image},
            HTTP_HX_REQUEST='true'
        )
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'image_url' in response.json()


@pytest.mark.django_db
class TestAdminViews:
    """Test the admin views."""

    def test_admin_user_list(self, client, admin_user, user):
        """Test the admin user list view."""
        client.force_login(admin_user)
        response = client.get(reverse('users:admin_user_list'))
        assert response.status_code == 200
        assert 'users' in response.context
        assert len(response.context['users']) >= 2  # At least admin_user and user
        assert user in response.context['users']
        assert admin_user in response.context['users']

    def test_admin_user_list_access_denied(self, client, user):
        """Test that regular users can't access admin views."""
        client.force_login(user)
        response = client.get(reverse('users:admin_user_list'))
        assert response.status_code == 302  # Redirect to login page

    def test_admin_user_create_get(self, client, admin_user):
        """Test getting the admin user create form."""
        client.force_login(admin_user)
        response = client.get(reverse('users:admin_user_create'))
        assert response.status_code == 200
        assert 'form' in response.context
        assert isinstance(response.context['form'], AdminUserForm)

    def test_admin_user_create_post(self, client, admin_user, admin_user_form_data):
        """Test creating a new user as admin."""
        client.force_login(admin_user)
        response = client.post(reverse('users:admin_user_create'), admin_user_form_data)
        assert response.status_code == 302
        assert response.url == reverse('users:admin_user_list')

        # Verify user was created
        assert User.objects.filter(username='newuser').exists()

    def test_admin_user_edit_get(self, client, admin_user, user):
        """Test getting the admin user edit form."""
        client.force_login(admin_user)
        response = client.get(reverse('users:admin_user_edit', args=[user.id]))
        assert response.status_code == 200
        assert 'form' in response.context
        assert 'profile_form' in response.context
        assert isinstance(response.context['form'], AdminUserForm)
        assert response.context['form'].instance == user

    def test_admin_user_edit_post(self, client, admin_user, user):
        """Test editing a user as admin."""
        client.force_login(admin_user)
        edit_data = {
            'username': user.username,
            'email': 'edited@example.com',
            'first_name': 'Edited',
            'last_name': 'User',
            'is_active': True,
            'is_staff': True,
            'is_superuser': False,
            # Profile fields
            'bio': 'Edited bio',
            'position': 'Manager',
            'department': 'HR',
            'phone_number': '555-987-6543'
        }
        response = client.post(reverse('users:admin_user_edit', args=[user.id]), edit_data)
        assert response.status_code == 302
        assert response.url == reverse('users:admin_user_list')

        # Verify user was updated
        user.refresh_from_db()
        user.profile.refresh_from_db()
        assert user.email == 'edited@example.com'
        assert user.first_name == 'Edited'
        assert user.is_staff
        assert user.profile.bio == 'Edited bio'
        assert user.profile.department == 'HR'

    def test_admin_user_delete_get(self, client, admin_user, user):
        """Test getting the admin user delete confirmation."""
        client.force_login(admin_user)
        response = client.get(
            reverse('users:admin_user_delete', args=[user.id]),
            HTTP_HX_REQUEST='true'
        )
        assert response.status_code == 200
        assert 'user_obj' in response.context
        assert response.context['user_obj'] == user

    def test_admin_user_delete_post(self, client, admin_user, user):
        """Test deleting a user as admin."""
        client.force_login(admin_user)
        user_id = user.id
        response = client.post(reverse('users:admin_user_delete', args=[user_id]))
        assert response.status_code == 302
        assert response.url == reverse('users:admin_user_list')

        # Verify user was deleted
        assert not User.objects.filter(id=user_id).exists()


# -------------------- TEMPLATE TAG TESTS --------------------


@pytest.mark.django_db
class TestUserTemplateTags:
    """Test the user template tags."""

    def test_full_name_or_username_full_name(self, user):
        """Test full_name_or_username with a user that has a full name."""
        user.first_name = 'Test'
        user.last_name = 'User'
        user.save()
        assert full_name_or_username(user) == 'Test User'

    def test_full_name_or_username_username(self, user):
        """Test full_name_or_username with a user that has no full name."""
        user.first_name = ''
        user.last_name = ''
        user.save()
        assert full_name_or_username(user) == user.username

    def test_profile_image_url_with_image(self, user, mock_image):
        """Test profile_image_url when user has a profile image."""
        user.profile.profile_image = mock_image
        user.profile.save()
        assert profile_image_url(user) == user.profile.profile_image.url

    def test_profile_image_url_without_image(self, user):
        """Test profile_image_url when user has no profile image."""
        user.profile.profile_image = None
        user.profile.save()
        assert profile_image_url(user) == ''

    def test_user_role_admin(self, admin_user):
        """Test user_role with admin user."""
        assert user_role(admin_user) == 'Admin'

    def test_user_role_staff(self, staff_user):
        """Test user_role with staff user."""
        assert user_role(staff_user) == 'Staff'

    def test_user_role_regular(self, user):
        """Test user_role with regular user."""
        assert user_role(user) == 'User'

    def test_auth_user_display(self, user):
        """Test auth_user_display with a user."""
        # This function uses allauth's user_display function
        # Just testing that it returns something for a user
        assert auth_user_display(user)

    def test_auth_status_badge_admin(self, admin_user):
        """Test auth_status_badge with admin user."""
        badge = auth_status_badge(admin_user)
        assert 'auth-badge-admin' in badge
        assert '>Admin<' in badge

    def test_auth_status_badge_staff(self, staff_user):
        """Test auth_status_badge with staff user."""
        badge = auth_status_badge(staff_user)
        assert 'auth-badge-staff' in badge
        assert '>Staff<' in badge

    def test_auth_status_badge_user(self, user):
        """Test auth_status_badge with regular user."""
        badge = auth_status_badge(user)
        assert 'auth-badge-user' in badge
        assert '>User<' in badge

    def test_auth_status_badge_anonymous(self):
        """Test auth_status_badge with anonymous user."""
        from django.contrib.auth.models import AnonymousUser
        badge = auth_status_badge(AnonymousUser())
        assert 'auth-badge-guest' in badge
        assert '>Guest<' in badge

    @patch('users.templatetags.user_tags.EmailAddress')
    def test_has_verified_email_true(self, mock_email_address, user):
        """Test has_verified_email when user has verified email."""
        mock_email_address.objects.filter.return_value.exists.return_value = True
        assert has_verified_email(user) is True

    @patch('users.templatetags.user_tags.EmailAddress')
    def test_has_verified_email_false(self, mock_email_address, user):
        """Test has_verified_email when user has no verified email."""
        mock_email_address.objects.filter.return_value.exists.return_value = False
        assert has_verified_email(user) is False

    def test_has_verified_email_anonymous(self):
        """Test has_verified_email with anonymous user."""
        from django.contrib.auth.models import AnonymousUser
        assert has_verified_email(AnonymousUser()) is False
