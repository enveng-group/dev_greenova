from _typeshed import Incomplete
from django.utils.deprecation import MiddlewareMixin

logger: Incomplete

class ActiveCompanyMiddleware(MiddlewareMixin):
    def process_request(self, request) -> None: ...
