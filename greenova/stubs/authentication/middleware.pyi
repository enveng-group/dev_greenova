from _typeshed import Incomplete
from collections.abc import Callable as Callable
from django.http import HttpRequest, HttpResponse

logger: Incomplete

class CustomHttpRequest(HttpRequest):
    is_post_logout: bool

class LogoutStateMiddleware:
    get_response: Incomplete
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None: ...
    def __call__(self, request: CustomHttpRequest) -> HttpResponse: ...
