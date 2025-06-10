from typing import Any

from _typeshed import Incomplete
from beartype import beartype
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest

from .models import Obligation as Obligation

logger: Incomplete

class ObligationContextMixin:
    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...

class ObligationPermissionRequiredMixin(PermissionRequiredMixin):
    permission_required: str
    @beartype
    def has_permission(self) -> bool: ...
    @beartype
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Any: ...
