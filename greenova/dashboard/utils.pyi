from typing import Any

from django.db.models import QuerySet

@beartype
def sanitize_html(
    value: str,
    tags: list[str] | None = ...,
    attributes: dict[str, list[str]] | None = ...,
) -> str: ...
@beartype
def aggregate_dashboard_metrics(projects: QuerySet[Any]) -> dict[str, Any]: ...
@beartype
def user_has_dashboard_permission(user: Any, perm: str, obj: Any = ...) -> bool: ...
@beartype
def get_objects_user_can_view(
    user: Any, queryset: QuerySet[Any], perm: str
) -> list[Any]: ...
