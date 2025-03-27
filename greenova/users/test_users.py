"""
Unit tests for user functionality using pytest and pytest-django.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest

from .models import Profile

User = get_user_model()


@pytest.fixture
def user_profile(regular_user):
    """Create a profile for the regular user."""
    profile, _ = Profile.objects.get_or_create(
        user=regular_user,
        defaults={
            'bio': '',
            'position': '',
            'department': '',
            'phone_number': '',
            'profile_image': None,
        }
    )
    return profile


@pytest.mark.django_db
class testCRUD:
    """Test user CRUD operations."""

    def test_user_creation(self, regular_user, user_profile):
        """Test user creation."""
        assert User.objects.count() >= 1
        assert Profile.objects.count() >= 1

    def test_user_update(self, regular_user):
        """Test user update."""
        regular_user.first_name = 'Updated'
        regular_user.save()
        db_user = User.objects.get(id=regular_user.id)
        assert db_user.first_name == 'Updated'

    def test_user_deletion(self, regular_user, user_profile):
        """Test user deletion."""
        user_id = regular_user.id
        profile_id = user_profile.id
        regular_user.delete()
        assert not User.objects.filter(id=user_id).exists()
        assert not Profile.objects.filter(id=profile_id).exists()

    def test_admin_user_list_view(self, admin_client):
        """Test admin user list view."""
        response = admin_client.get(reverse('users:admin_user_list'))
        assert response.status_code == 200
        assert b'test' in response.content

    def test_admin_user_create_view(self, admin_client):
        """Test admin user creation view."""
        response = admin_client.post(
            reverse('users:admin_user_create'),
            {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'Newpass123!',
                'password2': 'Newpass123!',
                'is_active': True,
            },
        )
        assert response.status_code == 302
        assert User.objects.filter(username='newuser').exists()

    def test_admin_user_edit_view(self, admin_client, regular_user):
        """Test admin user edit view."""
        response = admin_client.post(
            reverse('users:admin_user_edit', args=[regular_user.id]),
            {
                'username': 'updateduser',
                'email': 'updateduser@example.com',
                'is_active': True,
            },
        )
        assert response.status_code == 302
        regular_user.refresh_from_db()
        assert regular_user.username == 'updateduser'

    def test_admin_user_delete_view(self, admin_client, regular_user):
        """Test admin user delete view."""
        user_id = regular_user.id
        response = admin_client.post(reverse('users:admin_user_delete', args=[user_id]))
        assert response.status_code == 302
        assert not User.objects.filter(id=user_id).exists()


@pytest.mark.django_db
class testReset:
    """Test password reset functionality."""

    def test_password_reset_request(self, client, regular_user):
        """Test password reset request."""
        response = client.post(
            reverse('account_reset_password'),
            {'email': regular_user.email},
        )
        assert response.status_code == 302

    def test_password_reset_confirm(self, client, regular_user):
        """Test password reset confirmation."""
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode

        uid = urlsafe_base64_encode(force_bytes(regular_user.pk))
        token = default_token_generator.make_token(regular_user)

        response = client.post(
            reverse('account_reset_password_from_key', args=[uid, token]),
            {
                'password1': 'newpassword123',
                'password2': 'newpassword123',
            },
        )
        assert response.status_code == 302
        regular_user.refresh_from_db()
        assert regular_user.check_password('newpassword123')
