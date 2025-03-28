import re

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

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
        data = {
            'username': 'test1',
            'email': 'test1@example.com',
            'password1': 'test-U$3r-0nE',
            'password2': 'test-U$3r-0nE'
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
        user = django_user_model.objects.create_user(
            username='emailuser',
            email='emailuser@example.com',
            password='test'
        )
        user.is_active = True
        user.save()

        url = reverse('account_login')
        data = {
            'login': 'emailuser@example.com',
            'password': 'test'
        }

        response = client.post(url, data)

        # Should redirect after login
        assert response.status_code == 302
        # Verify user is logged in
        assert response.wsgi_request.user.is_authenticated

    def test_login_with_username(self, client, django_user_model):
        """Test user can login with username."""
        # Create a verified user
        user = django_user_model.objects.create_user(
            username='test',
            email='test@example.com',
            password='test'
        )
        user.is_active = True
        user.save()

        url = reverse('account_login')
        data = {
            'login': 'test',
            'password': 'test'
        }

        response = client.post(url, data)

        # Should redirect after login
        assert response.status_code == 302
        # Verify user is logged in
        assert response.wsgi_request.user.is_authenticated

    def test_logout(self, client, django_user_model):
        """Test user can logout."""
        # Create and login a user
        user = django_user_model.objects.create_user(
            username='logoutuser',
            password='test'
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
        # Create and login a user
        user = django_user_model.objects.create_user(
            username='changepassuser',
            password='OldPassword123!'
        )
        client.force_login(user)

        url = reverse('account_change_password')
        data = {
            'oldpassword': 'OldPassword123!',
            'password1': 'NewPassword456!',
            'password2': 'NewPassword456!'
        }

        response = client.post(url, data)

        # Should redirect after password change
        assert response.status_code == 302

        # Test login with new password
        client.logout()
        login_data = {
            'login': 'changepassuser',
            'password': 'NewPassword456!'
        }

        login_response = client.post(reverse('account_login'), login_data)
        assert login_response.status_code == 302
        assert login_response.wsgi_request.user.is_authenticated

    def test_password_reset_request(self, client, django_user_model, mailoutbox):
        """Test password reset request sends email."""
        # Create a user
        user = django_user_model.objects.create_user(
            username='resetuser',
            email='reset@example.com',
            password='test'
        )

        url = reverse('account_reset_password')
        data = {
            'email': 'reset@example.com'
        }

        response = client.post(url, data)

        # Should redirect to password reset done page
        assert response.status_code == 302
        assert reverse('account_reset_password_done') in response['Location']

        # Check that an email was sent
        assert len(mailoutbox) == 1
        assert mailoutbox[0].subject == 'Password Reset'
        assert 'reset@example.com' in mailoutbox[0].to

        # Extract reset link from email
        email_body = mailoutbox[0].body
        reset_links = re.findall(r'http://testserver(/.*?/)', email_body)
        assert len(reset_links) > 0
        reset_link = reset_links[0]

        # Test reset link works
        response = client.get(reset_link)
        assert response.status_code == 200
        assert 'Change Password' in response.content.decode()

    def test_email_management(self, client, django_user_model):
        """Test user can manage emails."""
        # Create and login a user
        user = django_user_model.objects.create_user(
            username='emailuser',
            email='primary@example.com',
            password='test'
        )
        user.is_active = True
        user.save()
        client.force_login(user)

        # Test email page loads
        url = reverse('account_email')
        response = client.get(url)

        assert response.status_code == 200
        assert 'primary@example.com' in response.content.decode()

        # Test adding a new email
        data = {
            'email': 'secondary@example.com',
            'action_add': ''
        }

        response = client.post(url, data)

        assert response.status_code == 302  # Should redirect back to email page
        assert user.emailaddress_set.filter(email='secondary@example.com').exists()

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
        def mock_get_login_url(*args, **kwargs):
            return '/github/login/redirect'

        # Use monkeypatch to mock the method chain
        monkeypatch.setattr(
            'allauth.socialaccount.providers.github.views.GitHubOAuth2Adapter.get_provider',
            lambda *args, **kwargs: type('obj', (object,), {'get_login_url': mock_get_login_url})()
        )

        # We need to be logged in to test connections
        user = User.objects.create_user(username='socialuser', password='password')
        client.force_login(user)

        response = client.get(url)
        assert response.status_code == 200

    def test_social_connections_page(self, client, django_user_model):
        """Test social connections page loads for authenticated users."""
        # Create and login a user
        user = django_user_model.objects.create_user(
            username='connectuser',
            password='test'
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
        user = django_user_model.objects.create_user(
            username='sessionuser',
            password='test'
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
        user = django_user_model.objects.create_user(
            username='sessionuser2',
            password='test'
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
        user = django_user_model.objects.create_user(
            username='mfauser',
            password='test'
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
        pass

    @pytest.mark.skip('Requires WebAuthn hardware')
    def test_webauthn_registration(self, client, django_user_model):
        """Test WebAuthn registration flow."""
        # This test would require mocking WebAuthn hardware
        # which is complex for a unit test
        pass

    @pytest.mark.skip('Requires MFA setup')
    def test_recovery_codes_generation(self, client, django_user_model):
        """Test recovery codes generation."""
        # This test would require setting up MFA first
        pass

# UI Tests with Selenium
@pytest.mark.django_db
class TestAuthenticationUI:
    """Test authentication UI with Selenium."""

    def test_login_form_ui(self, live_server, selenium):
        """Test login form UI and basic interactions."""
        # Visit the login page
        selenium.get(f'{live_server.url}/accounts/login/')

        # Check page title and form elements
        assert 'Sign In' in selenium.title

        # Check form fields
        username_input = selenium.find_element(By.NAME, 'login')
        password_input = selenium.find_element(By.NAME, 'password')
        submit_button = selenium.find_element(By.XPATH, "//button[@type='submit']")

        # Verify they exist
        assert username_input.is_displayed()
        assert password_input.is_displayed()
        assert submit_button.is_displayed()

        # Verify submit button text
        assert 'Sign In' in submit_button.text

        # Check for "Sign Up" link
        signup_link = selenium.find_element(By.XPATH, "//a[contains(@href, '/accounts/signup/')]")
        assert signup_link.is_displayed()
        assert 'sign up' in signup_link.text.lower()

    def test_signup_form_ui(self, live_server, selenium):
        """Test signup form UI and basic interactions."""
        # Visit the signup page
        selenium.get(f'{live_server.url}/accounts/signup/')

        # Check page title and form elements
        assert 'Sign Up' in selenium.title

        # Check form fields
        username_input = selenium.find_element(By.NAME, 'username')
        email_input = selenium.find_element(By.NAME, 'email')
        password1_input = selenium.find_element(By.NAME, 'password1')
        password2_input = selenium.find_element(By.NAME, 'password2')
        submit_button = selenium.find_element(By.XPATH, "//button[@type='submit']")

        # Verify they exist
        assert username_input.is_displayed()
        assert email_input.is_displayed()
        assert password1_input.is_displayed()
        assert password2_input.is_displayed()
        assert submit_button.is_displayed()

        # Verify submit button text
        assert 'Sign Up' in submit_button.text

    def test_login_workflow(self, live_server, selenium, django_user_model):
        """Test full login workflow with Selenium."""
        # Create a test user
        user = django_user_model.objects.create_user(
            username='seleniumuser',
            password='SeleniumTest123!',
            email='selenium@example.com',
            is_active=True
        )

        # Visit the login page
        selenium.get(f'{live_server.url}/accounts/login/')

        # Fill in the login form
        username_input = selenium.find_element(By.NAME, 'login')
        password_input = selenium.find_element(By.NAME, 'password')
        submit_button = selenium.find_element(By.XPATH, "//button[@type='submit']")

        username_input.send_keys('seleniumuser')
        password_input.send_keys('SeleniumTest123!')
        submit_button.click()

        # Wait for redirect after login
        WebDriverWait(selenium, 10).until(
            lambda driver: driver.current_url != f'{live_server.url}/accounts/login/'
        )

        # Should redirect to dashboard after login
        assert '/dashboard/' in selenium.current_url

    def test_signup_workflow(self, live_server, selenium):
        """Test full signup workflow with Selenium."""
        import uuid
        unique_username = f'test_{uuid.uuid4().hex[:8]}'

        # Visit the signup page
        selenium.get(f'{live_server.url}/accounts/signup/')

        # Fill in the signup form
        username_input = selenium.find_element(By.NAME, 'username')
        email_input = selenium.find_element(By.NAME, 'email')
        password1_input = selenium.find_element(By.NAME, 'password1')
        password2_input = selenium.find_element(By.NAME, 'password2')
        submit_button = selenium.find_element(By.XPATH, "//button[@type='submit']")

        username_input.send_keys(unique_username)
        email_input.send_keys(f'{unique_username}@example.com')
        password1_input.send_keys('SignupTest123!')
        password2_input.send_keys('SignupTest123!')
        submit_button.click()

        # Wait for redirect after signup
        WebDriverWait(selenium, 10).until(
            lambda driver: driver.current_url != f'{live_server.url}/accounts/signup/'
        )

        # Usually redirects to email verification page
        assert 'verify' in selenium.page_source.lower() or 'confirm' in selenium.page_source.lower()

    def test_password_reset_ui(self, live_server, selenium):
        """Test password reset UI."""
        # Visit the password reset page
        selenium.get(f'{live_server.url}/accounts/password/reset/')

        # Check page title and form elements
        assert 'Password Reset' in selenium.title

        # Check form fields
        email_input = selenium.find_element(By.NAME, 'email')
        submit_button = selenium.find_element(By.XPATH, "//button[@type='submit']")

        # Verify they exist
        assert email_input.is_displayed()
        assert submit_button.is_displayed()

        # Verify submit button text
        assert 'Reset' in submit_button.text

    def test_accessibility_login_page(self, live_server, selenium):
        """Test accessibility features on login page."""
        selenium.get(f'{live_server.url}/accounts/login/')

        # Check for proper heading hierarchy
        h1_elements = selenium.find_elements(By.TAG_NAME, 'h1')
        assert len(h1_elements) == 1  # Should have exactly one h1
        assert 'Sign In' in h1_elements[0].text

        # Check that all form fields have labels or aria-label
        input_elements = selenium.find_elements(By.TAG_NAME, 'input')
        for input_element in input_elements:
            if input_element.get_attribute('type') not in ['hidden', 'submit']:
                # Either has a label element or aria-label attribute
                input_id = input_element.get_attribute('id')
                if input_id:
                    labels = selenium.find_elements(By.CSS_SELECTOR, f"label[for='{input_id}']")
                    aria_label = input_element.get_attribute('aria-label')
                    placeholder = input_element.get_attribute('placeholder')
                    assert len(labels) > 0 or aria_label or placeholder, f'Input {input_id} missing accessible label'

        # Check that buttons have text content
        buttons = selenium.find_elements(By.TAG_NAME, 'button')
        for button in buttons:
            assert button.text.strip() != '', 'Button has no text content'

        # Check for proper tab order - interactive elements should have positive or no tabindex
        interactive_elements = selenium.find_elements(
            By.CSS_SELECTOR, 'a, button, input, select, textarea'
        )
        for element in interactive_elements:
            tabindex = element.get_attribute('tabindex')
            if tabindex:
                assert int(tabindex) >= 0, f'Element has negative tabindex: {element.tag_name}'
