import logging
from enum import Enum
from typing import Any

from beartype import beartype
from django import template
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import format_html
from projects.models import Project

logger = logging.getLogger(__name__)

register = template.Library()


class ProjectRole(Enum):
    """Project role enumeration for template tags."""

    OWNER = "owner"
    MANAGER = "manager"
    MEMBER = "member"
    VIEWER = "viewer"


@register.inclusion_tag("obligations/components/tables/obligation_list.html")
def render_obligation_list(context: dict[str, Any]) -> dict[str, Any]:
    """Render the obligation list template with the given context.

    Args:
        context: The context data for the template.

    Returns:
        A dictionary containing the context data.

    """
    return context


@register.filter
@beartype
def get_item(dictionary: dict[str, Any], key: Any) -> Any:
    """Get item from dictionary by key."""
    return dictionary.get(key)


@register.filter
@beartype
def get_user_role(project: Project, user: AbstractUser) -> str:
    """Get user's role in project.

    Args:
        project: The project to check
        user: The user to get role for

    Returns:
        str: User's role or 'viewer' if none found

    """
    try:
        return project.get_user_role(user)
    except ObjectDoesNotExist as e:
        logger.exception("Error getting user role: %s", str(e))
        return ProjectRole.VIEWER.value


@register.filter
@beartype
def format_role(role: str) -> str:
    """Format role name for display."""
    return role.replace("_", " ").title()


@register.inclusion_tag("projects/components/role_badge.html")
def render_role_badge(context: dict[str, Any]) -> dict[str, Any]:
    """Render the role badge template with the given context.

    Args:
        context: The context data for the template.

    Returns:
        A dictionary containing the context data.

    """
    return context


@register.filter
@beartype
def transform_queryset(queryset: Any, method_name: str) -> list[Any]:
    """Call a method on each object in the queryset and return a list of results."""
    if method_name == "to_dict":
        return [{"id": str(obj.id), "name": obj.name} for obj in queryset]
    return [
        getattr(obj, method_name)()
        if callable(getattr(obj, method_name))
        else getattr(obj, method_name)
        for obj in queryset
    ]


@register.filter
@beartype
def to_list(value: Any) -> list[Any]:
    """Convert an iterable to a list."""
    return list(value)


@register.simple_tag
@beartype
def project_status_badge(status: str) -> str:
    """Generate a status badge for projects."""
    status_classes = {
        "active": "bg-green-100 text-green-800",
        "pending": "bg-yellow-100 text-yellow-800",
        "completed": "bg-blue-100 text-blue-800",
        "cancelled": "bg-red-100 text-red-800",
    }

    css_class = status_classes.get(status.lower(), "bg-gray-100 text-gray-800")

    return format_html(
        '<span class="badge {}">{}</span>',
        css_class,
        status.title(),
    )


@register.simple_tag
@beartype
def project_badge(project_type: str, display_text: str | None = None) -> str:
    """Generate a badge for project types with icon and text."""
    try:
        badge_config = get_badge_config(project_type)
    except ValueError as e:
        logger.exception("Error generating project badge: %s", str(e))
        return ""

    return format_html(
        '<span class="inline-flex items-center px-3 py-0.5 '
        'rounded-full text-sm font-medium {}">{}</span>',
        badge_config["css_class"],
        display_text or project_type.title(),
    )


@beartype
def get_badge_config(project_type: str) -> dict[str, str]:
    """Get badge configuration for a project type."""
    badge_configs = {
        "environmental": {
            "css_class": "bg-green-100 text-green-800",
        },
        "compliance": {
            "css_class": "bg-blue-100 text-blue-800",
        },
        "monitoring": {
            "css_class": "bg-yellow-100 text-yellow-800",
        },
    }

    config = badge_configs.get(project_type.lower())
    if not config:
        msg = f"Unsupported project type: {project_type}"
        raise ValueError(msg)

    return config


@register.inclusion_tag("projects/partials/project_list.html")
def render_project_list(context: dict[str, Any]) -> dict[str, Any]:
    """Render the project list template with the given context.

    Args:
        context: The context data for the template.

    Returns:
        A dictionary containing the context data.

    """
    return context


@register.simple_tag
@beartype
def get_site_name(site_name: str | None = None) -> str:
    """Return the site name or default."""
    return site_name or "Greenova"


@register.simple_tag
@beartype
def get_site_version(site_version: str | None = None) -> str:
    """Return the site version or default."""
    return site_version or "1.0.0"


@register.filter
@beartype
def feature_enabled(feature_flags: dict[str, Any], feature: str) -> bool:
    """Check if a feature flag is enabled."""
    return feature_flags.get(feature, False)


@register.simple_tag
@beartype
def get_current_project(current_project: Any = None) -> Any:
    """Return the current project or None."""
    return current_project


@register.simple_tag
@beartype
def get_user_projects(user_projects: Any = None) -> Any:
    """Return the queryset of user projects or empty queryset."""
    return user_projects or []


@register.simple_tag
@beartype
def get_project_status_summary(
    project_status_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return the project status summary dict or empty dict."""
    return project_status_summary or {}
