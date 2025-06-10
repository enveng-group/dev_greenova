"""Copyright (C) 2024 Adrian Gallo <agallo@enveng-group.com.au>
This file is part of Greenova and is licensed under the AGPL-3.0.

Dashboard app utilities for Greenova.

Security and sanitization helpers (bleach, permissions).
"""

from typing import Any

import bleach
from beartype import beartype
from django.db.models import QuerySet
from guardian.shortcuts import get_objects_for_user


@beartype
def sanitize_html(
    value: str,
    tags: list[str] | None = None,
    attributes: dict[str, list[str]] | None = None,
) -> str:
    """Sanitize HTML input using bleach.

    Args:
        value: The HTML string to sanitize.
        tags: Optional list of allowed HTML tags.
        attributes: Optional dict of allowed attributes per tag.

    Returns:
        The sanitized HTML string.

    """
    allowed_tags = tags or [
        "b",
        "i",
        "u",
        "em",
        "strong",
        "a",
        "ul",
        "ol",
        "li",
        "p",
        "br",
        "span",
    ]
    allowed_attrs = attributes or {"a": ["href", "title", "target"], "span": ["class"]}
    return bleach.clean(
        value,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True,
    )


@beartype
def aggregate_dashboard_metrics(projects: QuerySet[Any]) -> dict[str, Any]:
    """Aggregate dashboard metrics from a queryset of projects.

    Args:
        projects: QuerySet of Project objects.

    Returns:
        dict[str, Any]: Aggregated metrics (total, active, completed).

    """
    total = projects.count()
    active = (
        projects.filter(status="active").count()
        if hasattr(projects.model, "status")
        else 0
    )
    completed = (
        projects.filter(status="completed").count()
        if hasattr(projects.model, "status")
        else 0
    )
    return {
        "total_projects": total,
        "active_projects": active,
        "completed_projects": completed,
    }


def user_has_dashboard_permission(user: Any, perm: str, obj: Any = None) -> bool:
    """Check if a user has a specific dashboard permission, optionally object-level.

    Args:
        user: The user to check (User or AnonymousUser).
        perm: The permission codename (e.g., 'dashboard.view_dashboard').
        obj: Optional object for object-level permission.

    Returns:
        bool: True if the user has the permission, else False.

    """
    if not user or not getattr(user, "is_authenticated", False):
        return False
    if obj is not None:
        return user.has_perm(perm, obj)
    return user.has_perm(perm)


@beartype
def get_objects_user_can_view(
    user: Any, queryset: QuerySet[Any], perm: str
) -> list[Any]:
    """Get all objects of a queryset the user has view permission for (guardian).

    Args:
        user: The user to check (User or AnonymousUser).
        queryset: The model queryset (e.g., Model.objects.all()).
        perm: The permission codename (e.g., 'dashboard.view_dashboard').

    Returns:
        list[Any]: Objects the user can view.

    """
    if not user or not getattr(user, "is_authenticated", False):
        return []
    return get_objects_for_user(user, perm, klass=queryset)
