from typing import Any

from beartype import beartype
from django.http import HttpRequest, HttpResponse

class ProjectPermissionRequiredMixin:
    required_roles: list[str]
    error_message: str
    def dispatch(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse: ...

class ProjectContextMixin:
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...

@beartype
def user_has_obligation_role(user: Any, obligation: Any, roles: list[str]) -> bool: ...

class ObligationPermissionRequiredMixin:
    required_roles: list[str]
    error_message: str
    def dispatch(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse: ...

class ObligationContextMixin:
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...
