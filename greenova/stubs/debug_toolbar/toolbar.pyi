from typing import Any, Callable, Dict, Optional

from django.http import HttpRequest, HttpResponse, HttpResponseBase

class DebugToolbar:
    def __init__(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None: ...
    def process_request(self, request: HttpRequest) -> None: ...
    def process_view(
        self,
        request: HttpRequest,
        view_func: Callable,
        view_args: Any,
        view_kwargs: Dict[str, Any],
    ) -> Optional[HttpResponse]: ...
    def process_response(
        self, request: HttpRequest, response: HttpResponseBase
    ) -> HttpResponseBase: ...

def show_toolbar(request: HttpRequest) -> bool: ...
