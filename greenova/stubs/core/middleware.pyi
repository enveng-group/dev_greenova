from _typeshed import Incomplete
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin

logger: Incomplete

class ProjectSelectionMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest): ...
