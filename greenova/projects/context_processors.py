"""Custom context processors for the projects app.

Provides project info (current project, project list, permissions) for templates.

Returns:
    dict: Context variables for templates.
"""
from typing import Any, Dict
from beartype import beartype
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Project
from django.db.models import Q

@beartype
def projects_context(request) -> Dict[str, Any]:
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
            Q(members=user) | Q(owner=user)
        ).distinct()
        # Current project from session or GET param
        project_id = request.session.get("current_project_id") or request.GET.get("project_id")
        if project_id:
            current_project = user_projects.filter(id=project_id).first()
        # Project status summary (example: active/inactive)
        project_status_summary = {
            "active": user_projects.filter(is_active=True).count(),
            "inactive": user_projects.filter(is_active=False).count(),
            "total": user_projects.count(),
        }
    return {
        "current_project": current_project,
        "user_projects": user_projects,
        "project_status_summary": project_status_summary,
    }
