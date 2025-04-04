"""Authentication tests for the Greenova project.

IMPORTANT: When running bandit on this file, use:
    bandit -r /path/to/file --skip B101
or use the project-level command that respects .banditrc/.banditignore
"""
# nosec
import os
import re

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse

User = get_user_model()

# Basic Authentication Tests
@pytest.mark.django_db
class TestAuthentication:
    """Test basic authentication functionality."""

    def test_login_page_loads(self, client):
        """Test login page loads correctly."""
        url = reverse('account_login')
        response = client.get(url)

        assert response.status_code == 200
        assert 'Sign In' in response.content.decode()

    def test_signup_page_loads(self, client):
        """Test signup page loads correctly."""
        url = reverse('account_signup')
        response = client.get(url)

        assert response.status_code == 200
        assert 'Sign Up' in response.content.decode()

    def test_logout_requires_login(self, client):
        """Test logout page requires authentication."""
        url = reverse('account_logout')
        response = client.get(url)

        # Should redirect to login page
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    def test_password_change_requires_login(self, client):
        """Test password change page requires authentication."""
        url = reverse('account_change_password')
        response = client.get(url)

        login_url = reverse('account_login')

        # Should redirect to login page
        assert response.status_code == 302
        assert login_url in response['Location']

    def test_password_reset_page_loads(self, client):
        """Test password reset page loads correctly."""
        url = reverse('account_reset_password')
        response = client.get(url)

        assert response.status_code == 200
        assert 'Password Reset' in response.content.decode()

# Account Management Tests
@pytest.mark.django_db
class TestAccountManagement:
    """Test django-allauth account management functionality."""

    def test_user_signup(self, client):
        """Test user can sign up."""
        url = reverse('account_signup')
        secure_password = os.environ.get('TEST_SECURE_PASSWORD', 'test-U$3r-0nE')
        test_email = os.environ.get('TEST_EMAIL', 'test1@example.com')

        data = {
            'username': 'test1',
            'email': test_email,
            'password1': secure_password,
            'password2': secure_password
        }

        response = client.post(url, data)

        # Should redirect after signup
        assert response.status_code == 302

        # Verify user was created
        assert User.objects.filter(username='test1').exists()

        # Verify email verification is required
        user = User.objects.get(username='test1')
        assert not user.is_active

    def test_login_with_email(self, client, django_user_model):
        """Test user can login with email."""
        # Create a verified user
        test_email = os.environ.get('TEST_EMAIL', 'emailuser@example.com')
        test_password = os.environ.get('TEST_PASSWORD', 'test')

        user = django_user_model.objects.create_user(
            username=os.environ.get('TEST_USERNAME', 'emailuser'),
            email=test_email,
            password=test_password
        )
        user.is_active = True
        user.save()

        url = reverse('account_login')
        data = {
            'login': test_email,
            'password': test_password
        }

        response = client.post(url, data)

        # Should redirect after login
        assert response.status_code == 302
        # Verify user is logged in
        assert response.wsgi_request.user.is_authenticated

    def test_login_with_username(self, client, django_user_model):
        """Test user can login with username."""
        # Create a verified user
        test_username = os.environ.get('TEST_USERNAME', 'test')
        test_email = os.environ.get('TEST_EMAIL', 'test@example.com')
        test_password = os.environ.get('TEST_PASSWORD', 'test')

        user = django_user_model.objects.create_user(
            username=test_username,
            email=test_email,
            password=test_password
        )
        user.is_active = True
        user.save()

        url = reverse('account_login')
        data = {
            'login': test_username,
            'password': test_password
        }

        response = client.post(url, data)

        # Should redirect after login
        assert response.status_code == 302
        # Verify user is logged in
        assert response.wsgi_request.user.is_authenticated

    def test_logout(self, client, django_user_model):
        """Test user can logout."""
        # Create and login a user
        test_username = os.environ.get('TEST_USERNAME', 'logoutuser')
        test_password = os.environ.get('TEST_PASSWORD', 'test')

        user = django_user_model.objects.create_user(
            username=test_username,
            password=test_password
        )
        client.force_login(user)

        url = reverse('account_logout')
        response = client.post(url)

        # Should redirect after logout
        assert response.status_code == 302

        # Get a new page to check if user is logged out
        response = client.get(reverse('account_login'))
        assert not response.wsgi_request.user.is_authenticated

    def test_password_change(self, client, django_user_model):
        """Test user can change password."""
        test_username = os.environ.get('TEST_USERNAME', 'changepassuser')
        test_password = os.environ.get('TEST_PASSWORD', 'OldPassword123!')

        # Create and login a user
        user = django_user_model.objects.create_user(
            username=test_username,
            password=test_password
        )
        client.force_login(user)

        url = reverse('account_change_password')
        data = {
            'oldpassword': test_password,
            'password1': 'NewPassword456!',
            'password2': 'NewPassword456!'
        }

        response = client.post(url, data)

        # Should redirect after password change
        assert response.status_code == 302

        # Test login with new password
        client.logout()
        login_data = {
            'login': test_username,
            'password': os.environ.get('TEST_NEW_PASSWORD', 'NewPassword456!')
        }

        login_response = client.post(reverse('account_login'), login_data)
        assert login_response.status_code == 302
        assert login_response.wsgi_request.user.is_authenticated

    def test_password_reset_request(self, client, django_user_model, mailoutbox):
        """Test password reset request sends email."""
        # Create a user
        test_username = os.environ.get('TEST_USERNAME', 'resetuser')
        test_email = os.environ.get('TEST_EMAIL', 'reset@example.com')
        test_password = os.environ.get('TEST_PASSWORD', 'test')

        # Create user directly
        user = django_user_model.objects.create_user(
            username=test_username,
            email=test_email,
            password=test_password
        )

        url = reverse('account_reset_password')
        data = {
            'email': test_email
        }
        # Verify the user exists before requesting password reset
        assert django_user_model.objects.filter(email=test_email).exists()
        # Verify user attributes
        assert user.email == test_email
        assert user.username == test_username

        response = client.post(url, data)

        # Should redirect to password reset done page
        assert response.status_code == 302
        assert reverse('account_reset_password_done') in response['Location']

        # Check that an email was sent
        assert len(mailoutbox) == 1
        assert mailoutbox[0].subject == 'Password Reset'
        assert test_email in mailoutbox[0].to

        # Extract reset link from email
        email_body = mailoutbox[0].body
        reset_links = re.findall(r'https://testserver(/.*?/)', email_body)
        assert len(reset_links) > 0
        reset_link = reset_links[0]

        # Test reset link works
        response = client.get(reset_link)
        assert response.status_code == 200
        assert 'Change Password' in response.content.decode()

    def test_reset_password_confirm(self, client, django_user_model, mailoutbox):
        """Test resetting password with confirmation code."""
        # Create a user
        test_username = os.environ.get('TEST_USERNAME', 'resetuser')
        test_email = os.environ.get('TEST_EMAIL', 'reset@example.com')
        test_password = os.environ.get('TEST_PASSWORD', 'old_password')
        new_password = os.environ.get('TEST_NEW_PASSWORD', 'new_password123')

        django_user_model.objects.create_user(
            username=test_username,
            email=test_email,
            password=test_password
        )

        # Request password reset
        url = reverse('account_reset_password')
        client.post(url, {'email': test_email})

        # Extract token and uid from the email
        email_body = mailoutbox[0].body
        reset_links = re.findall(r'https://testserver(/.*?/)', email_body)
        reset_url = reset_links[0]

        # Visit reset URL and set new password
        response = client.get(reset_url)
        assert response.status_code == 200

        # Extract form data from the page
        form_data = {
            'password1': new_password,
            'password2': new_password
        }

        response = client.post(reset_url, form_data)
        assert response.status_code == 302

        # Test login with new password
        client.login(username=test_username, password=new_password)
        response = client.get(reverse('account_login'))
        assert response.wsgi_request.user.is_authenticated

    def test_email_management(self, client, django_user_model):
        """Test user can manage emails."""
        # Create and login a user
        test_username = os.environ.get('TEST_USERNAME', 'emailuser')
        test_email = os.environ.get('TEST_EMAIL', 'primary@example.com')
        test_password = os.environ.get('TEST_PASSWORD', 'test')

        user = django_user_model.objects.create_user(
            username=test_username,
            email=test_email,
            password=test_password
        )
        user.is_active = True
        user.save()
        client.force_login(user)

        # Test email page loads
        url = reverse('account_email')
        response = client.get(url)

        assert response.status_code == 200
        assert test_email in response.content.decode()

        # Test adding a new email
        secondary_email = os.environ.get('SECONDARY_EMAIL', 'secondary@example.com')
        data = {
            'email': secondary_email,
            'action_add': ''
        }

        response = client.post(url, data)

        assert response.status_code == 302  # Should redirect back to email page
        assert user.emailaddress_set.filter(email=secondary_email).exists()

# Social Authentication Tests
@pytest.mark.django_db
class TestSocialAuthentication:
    """Test social authentication with GitHub."""

    def test_github_login_button_exists(self, client):
        """Test GitHub login button appears on login page."""
        url = reverse('account_login')
        response = client.get(url)

        assert response.status_code == 200
        content = response.content.decode()

        # Check for GitHub provider in the list
        assert 'Sign in with a third-party' in content

        # One of these patterns should match depending on the template
        assert ('GitHub' in content or
                'github' in content or
                'provider_id="github"' in content)

    def test_github_redirect(self, monkeypatch, client):
        """Test GitHub authentication redirects correctly."""
        url = reverse('socialaccount_connections')

        # Mock the response to avoid actual API calls
        def mock_get_login_url(*_args, **_kwargs):
            return '/github/login/redirect'

        # Use monkeypatch to mock the method chain
        monkeypatch.setattr(
            'allauth.socialaccount.providers.github.views.'
            'GitHubOAuth2Adapter.get_provider',
            lambda *args, **kwargs: type(
                'obj',
                (object,),
                {'get_login_url': mock_get_login_url}
            )()
        )

        # We need to be logged in to test connections
        test_username = os.environ.get('TEST_USERNAME', 'socialuser')
        test_password = os.environ.get('TEST_PASSWORD', 'password')

        # Create user and login
        created_user = User.objects.create_user(
            username=test_username,
            password=test_password
        )
        client.force_login(created_user)

        response = client.get(url)
        assert response.status_code == 200

    def test_social_connections_page(self, client, django_user_model):
        """Test social connections page loads for authenticated users."""
        # Create and login a user
        test_username = os.environ.get('TEST_USERNAME', 'connectuser')
        test_password = os.environ.get('TEST_PASSWORD', 'test')

        user = django_user_model.objects.create_user(
            username=test_username,
            password=test_password
        )
        client.force_login(user)

        url = reverse('socialaccount_connections')
        response = client.get(url)

        assert response.status_code == 200
        assert 'Account Connections' in response.content.decode()

# User Sessions Tests
@pytest.mark.django_db
class TestSessions:
    """Test user sessions management."""

    def test_session_list_requires_login(self, client):
        """Test session list page requires authentication."""
        url = reverse('usersessions_list')
        response = client.get(url)

        # Should redirect to login page
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    def test_user_sessions_page(self, client, django_user_model):
        """Test user sessions page loads for authenticated users."""
        # Create and login a user
        test_username = os.environ.get('TEST_USERNAME', 'sessionuser')
        test_password = os.environ.get('TEST_PASSWORD', 'test')

        user = django_user_model.objects.create_user(
            username=test_username,
            password=test_password
        )
        client.force_login(user)

        url = reverse('usersessions_list')
        response = client.get(url)

        assert response.status_code == 200
        assert 'Sessions' in response.content.decode()

        # The page should show the current session
        assert 'Started At' in response.content.decode()
        assert 'IP Address' in response.content.decode()
        assert 'Browser' in response.content.decode()

    def test_sign_out_other_sessions(self, client, django_user_model):
        """Test signing out other sessions."""
        # Create and login a user
        test_username = os.environ.get('TEST_USERNAME', 'sessionuser2')
        test_password = os.environ.get('TEST_PASSWORD', 'test')

        user = django_user_model.objects.create_user(
            username=test_username,
            password=test_password
        )
        client.force_login(user)

        # Create another session
        other_client = Client()
        other_client.force_login(user)

        # Test signing out other sessions
        url = reverse('usersessions_list')
        response = client.post(url)

        # Should redirect back to sessions page
        assert response.status_code == 302

# Multi-factor Authentication Tests
@pytest.mark.django_db
class TestMFA:
    """Test multi-factor authentication."""

    def test_mfa_index_requires_login(self, client):
        """Test MFA index page requires authentication."""
        url = reverse('mfa_index')
        response = client.get(url)

        # Should redirect to login page
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    def test_mfa_index_page(self, client, django_user_model):
        """Test MFA index page loads for authenticated users."""
        # Create and login a user
        test_username = os.environ.get('TEST_USERNAME', 'mfauser')
        test_password = os.environ.get('TEST_PASSWORD', 'test')

        user = django_user_model.objects.create_user(
            username=test_username,
            password=test_password
        )
        client.force_login(user)

        url = reverse('mfa_index')
        response = client.get(url)

        assert response.status_code == 200
        assert 'Two-Factor Authentication' in response.content.decode()

        # Check for MFA options based on settings
        content = response.content.decode()
        if 'totp' in settings.MFA_SUPPORTED_TYPES:
            assert 'Authenticator App' in content

        if 'webauthn' in settings.MFA_SUPPORTED_TYPES:
            assert 'Security Keys' in content

        if 'recovery_codes' in settings.MFA_SUPPORTED_TYPES:
            assert 'Recovery Codes' in content

    @pytest.mark.skip('Requires actual TOTP setup')
    def test_totp_activation(self, client, django_user_model):
        """Test TOTP activation flow."""
        # This test would require mocking the TOTP verification
        # or generating valid TOTP codes which is complex for a unit test

    @pytest.mark.skip('Requires WebAuthn hardware')
    def test_webauthn_registration(self, client, django_user_model):
        """Test WebAuthn registration flow."""
        # This test would require mocking WebAuthn hardware
        # which is complex for a unit test

    @pytest.mark.skip('Requires MFA setup')
    def test_recovery_codes_generation(self, client, django_user_model):
        """Test recovery codes generation."""
        # This test would require setting up MFA first
