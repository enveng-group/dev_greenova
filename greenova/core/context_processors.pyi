from typing import Any

from beartype import beartype
from django.http import HttpRequest

@beartype
def projects_context(request: HttpRequest) -> dict[str, Any]: ...
