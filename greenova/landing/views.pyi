from _typeshed import Incomplete
from beartype import beartype
from django.http import HttpRequest, HttpResponse

from .forms import NewsletterSignupForm as NewsletterSignupForm

logger: Incomplete

@beartype
def landing_page(request: HttpRequest) -> HttpResponse: ...
@beartype
def newsletter_signup(request: HttpRequest) -> HttpResponse: ...
