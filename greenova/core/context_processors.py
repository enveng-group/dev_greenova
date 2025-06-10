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
    """Provide project/user context for templates.

    Args:
        request: The current HTTP request.

    Returns:
        Context dictionary with project list, current project, and user info.

    """
    user = getattr(request, "user", None)
    projects = Project.objects.none()
    current_project = None
    if user and user.is_authenticated:
        projects = Project.objects.filter(
            Q(memberships__user=user) | Q(owner=user),
        ).distinct()
        current_project = getattr(request, "current_project", None)
    return {
        "project_list": projects,
        "current_project": current_project,
        "user": user,
    }
