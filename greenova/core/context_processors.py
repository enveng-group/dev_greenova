"""Global context processors for Greenova.

Provides project info (current project, project list, permissions) for templates.

Returns:
    dict: Context variables for templates.

"""

from typing import Any

from beartype import beartype
from django.db.models import Q
from django.http import HttpRequest
from projects.models import Project


@beartype
def projects_context(request: HttpRequest) -> dict[str, Any]:
    """Provide project and user context for templates.

    Args:
        request: The current HTTP request object.

    Returns:
        dict[str, Any]: Context with project list, current project, and user info.

    Example:
        >>> ctx = projects_context(request)
        >>> ctx["projects"]  # List[Project]
        >>> ctx["current_project"]  # Project | None
        >>> ctx["user"]  # User | None

    """
    user = getattr(request, "user", None)
    projects = Project.objects.none()
    current_project = None
    if user and getattr(user, "is_authenticated", False):
        projects = Project.objects.filter(
            Q(memberships__user=user) | Q(owner=user)
        ).distinct()
        current_project = getattr(request, "current_project", None)
    return {
        "project_list": projects,
        "projects": list(projects),
        "current_project": current_project,
        "user": user,
    }
