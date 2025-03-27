# Bug: Password Reset Confirmation Test Failing with Incorrect Status Code

## Issue Type

Bug

## Title

Bug: Password Reset Confirmation Test Failing with Incorrect Status Code

## Description

The password reset confirmation test is failing because it expects a redirect
(status code 302) after submitting a new password, but instead receives a
success page (status code 200). This indicates that the password reset flow in
the application doesn't match what the test expects.

## Current Behavior

When posting to the `account_reset_password_from_key` URL with new passwords,
the server responds with a 200 status code (success page) instead of
redirecting the user to another page with a 302 status code.

## Expected Behavior

After successful password reset confirmation, the application should redirect
the user (status code 302) to another page (likely a success page or login
page).

## Steps to Reproduce (for bugs)

1. Run the specific test:

```bash
pytest greenova/users/test_users.py::testReset::test_password_reset_confirm -v
```

2. The test failure occurs in the following code:

```python
def test_password_reset_confirm(self, client, regular_user):
    """Test password reset confirmation."""
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode

    uid = urlsafe_base64_encode(force_bytes(regular_user.pk))
    token = default_token_generator.make_token(regular_user)

    response = client.post(
        reverse("account_reset_password_from_key", args=[uid, token]),
        {
            "password1": "newpassword123",
            "password2": "newpassword123",
        },
    )
    assert response.status_code == 302  # This assertion fails
```

## Technical Context

- **Django Version**: 4.1.13
- **Python Version**: 3.9.21
- **Frontend Technologies**: PicoCSS, django-hyperscript, django-htmx
- **Database**: SQLite3 (development)
- **Affected Module/App**: users app (authentication flow)
- **Authentication Package**: django-allauth

## Proposed Implementation

Two possible solutions:

1. **Update test expectations**: If the current behavior (showing a success
   page with 200) is intentional, update the test to expect a 200 status code
   instead of 302.

2. **Fix the password reset flow**: If a redirect is expected, check the
   django-allauth configuration and customizations to ensure it properly
   redirects after password reset confirmation.

Specifically:

- Check if `ACCOUNT_PASSWORD_RESET_REDIRECT_URL` is properly set in settings.py
- Review any custom templates or views that might override django-allauth's
  default behavior
- Ensure the success URL is correctly configured for password reset flows

## Acceptance Criteria

- [ ] Test passes consistently
- [ ] Password reset flow works as expected in the actual application
- [ ] Implementation aligns with project's authentication requirements
- [ ] Flow meets WCAG 2.1 AA accessibility standards

## Additional Context

This is likely a configuration issue with django-allauth. The package supports
both returning a success page (200) or redirecting (302) after password reset,
depending on configuration.

Looking at
[django-allauth documentation](https://django-allauth.readthedocs.io/en/latest/configuration.html),
check if settings like `ACCOUNT_PASSWORD_RESET_REDIRECT_URL` or related
template overrides are affecting the expected behavior.

## Labels

bug, testing, authentication, django-allauth
