from _typeshed import Incomplete
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import TemplateView, View
from typing import Any

logger: Incomplete

class HomeRouterView(View):
    def get(self, request: HttpRequest) -> HttpResponse: ...

class HealthCheckView(View):
    def get(self, request: HttpRequest) -> JsonResponse: ...

class BaseTemplateView(TemplateView):
    def get_context_data(self, **kwargs) -> dict[str, Any]: ...
