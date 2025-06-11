from _typeshed import Incomplete
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from typing import Any, TypedDict

logger: Incomplete

class HtmxDetails(TypedDict, total=False):
    boosted: bool
    current_url: str
    history_restore_request: bool
    prompt: str
    target: str
    trigger: str
    trigger_name: str

class HomeView(TemplateView):
    template_name: str
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...

@require_POST
@csrf_protect
def newsletter_signup(request: HttpRequest) -> HttpResponse: ...
