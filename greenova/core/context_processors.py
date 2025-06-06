"""Global context processors for Greenova.

Provides project info (current project, project list, permissions) for templates.

Returns:
    dict: Context variables for templates.

"""

from typing import Any

from beartype import beartype
from django.db.models import Q
from projects.models import Project


@beartype
def projects_context(request) -> dict[str, Any]:
    """Inject project-related context variables into templates.

    Args:
        request: The current HttpRequest object.

    Returns:
        A dictionary of project-related context variables, including:
            - current_project: The user's selected project or None.
            - user_projects: Queryset of projects the user can access.
            - project_status_summary: Dict of project status counts.

    """
    user = getattr(request, "user", None)
    current_project = None
    user_projects = Project.objects.none()
    project_status_summary = {}
    if user and user.is_authenticated:
        # All projects user can access (view permission)
        user_projects = Project.objects.filter(
            Q(members=user) | Q(owner=user),
        ).distinct()
        # Current project from session or GET param

    return {
        "current_project": current_project,
        "user_projects": user_projects,
        "project_status_summary": project_status_summary,
    }
