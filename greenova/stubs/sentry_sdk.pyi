from typing import Any, Dict, List, Optional

# Placeholder for the sentry_sdk module
def init(
    dsn: Optional[str] = None,
    *,
    debug: bool = False,
    environment: Optional[str] = None,
    release: Optional[str] = None,
    traces_sample_rate: Optional[float] = None,
    integrations: Optional[List[Any]] = None,
    **options: Any,
) -> None: ...
def capture_message(message: str, level: Optional[str] = None) -> Any: ...
def capture_exception(error: Optional[Exception] = None) -> Any: ...
def add_breadcrumb(
    category: Optional[str] = None,
    message: Optional[str] = None,
    level: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
) -> None: ...

class Hub:
    def __init__(self, client: Any = None, scope: Any = None) -> None: ...
    def capture_message(self, message: str, level: Optional[str] = None) -> Any: ...
    def capture_exception(self, error: Optional[Exception] = None) -> Any: ...

current_hub = Hub()  # type: Hub
