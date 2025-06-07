from typing import Any

from _typeshed import Incomplete
from beartype import beartype

from .models import AuditLog
from .models import CustomUser as CustomUser

logger: Incomplete

@beartype
def log_audit_event(
    user: CustomUser | None,
    action: str,
    object_type: str = "",
    object_id: str = "",
    message: str = "",
    ip_address: str | None = None,
    extra_data: dict[str, Any] | None = None,
) -> None: ...
@beartype
def get_recent_audit_logs(limit: int = 50) -> list[AuditLog]: ...
