from typing import Any

# Placeholder for the sentry_sdk module
def init(
    dsn: str | None = None,
    *,
    debug: bool = False,
    environment: str | None = None,
    release: str | None = None,
    traces_sample_rate: float | None = None,
    integrations: list[Any] | None = None,
    **options: Any,
) -> None: ...
def capture_message(message: str, level: str | None = None) -> Any: ...
def capture_exception(error: Exception | None = None) -> Any: ...
def add_breadcrumb(
    category: str | None = None,
    message: str | None = None,
    level: str | None = None,
    data: dict[str, Any] | None = None,
) -> None: ...

class Hub:
    def __init__(self, client: Any = None, scope: Any = None) -> None: ...
    def capture_message(self, message: str, level: str | None = None) -> Any: ...
    def capture_exception(self, error: Exception | None = None) -> Any: ...

current_hub = Hub()  # type: Hub
