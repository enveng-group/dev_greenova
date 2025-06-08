from beartype import beartype
from django.test import TestCase

from .forms import NewsletterSignupForm as NewsletterSignupForm

class LandingPageTests(TestCase):
    @beartype
    def test_landing_page(self) -> None: ...

class NewsletterSignupFormTests(TestCase):
    @beartype
    def test_valid_email(self) -> None: ...
    @beartype
    def test_invalid_email(self) -> None: ...
    @beartype
    def test_email_sanitization(self) -> None: ...

class NewsletterSignupViewTests(TestCase):
    @beartype
    def test_newsletter_signup_success(self) -> None: ...
    @beartype
    def test_newsletter_signup_invalid_email(self) -> None: ...
