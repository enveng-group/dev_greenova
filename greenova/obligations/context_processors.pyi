from typing import Any

from beartype import beartype

from .models import Obligation as Obligation

@beartype
def obligations_context(request) -> dict[str, Any]: ...
