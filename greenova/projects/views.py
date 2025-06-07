"""Views for the projects app.

This module provides views for displaying, exporting, importing, and managing
project data, including permission checks and project membership.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import logging
from typing import Any, TypeVar, cast

import django_filters
from beartype import beartype
from core.mixins import ProjectContextMixin, ProjectPermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from guardian.shortcuts import assign_perm, get_objects_for_user

# from obligations.models import Obligation
from .models import Project, ProjectMembership
from .serializers import (
    ProjectCollectionProtoSerializer,
    ProjectMembershipProtoSerializer,
    ProjectProtoSerializer,
)
from .tables import ProjectTable

User = get_user_model()
logger = logging.getLogger(__name__)
T = TypeVar("T")


class ProjectFilter(django_filters.FilterSet):
    class Meta:
        model = Project
        fields = {
            "name": ["icontains"],
            "created_at": ["date__gte", "date__lte"],
        }


class ProjectListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    """List all projects the user can view, with filtering and table rendering."""

    model = Project
    table_class = ProjectTable
    template_name = "projects/project_list.html"
    filterset_class = ProjectFilter
    context_object_name = "object_list"

    def get_queryset(self) -> models.QuerySet[Project]:
        """Return queryset of projects the user can view."""
        allowed_projects = get_objects_for_user(
            self.request.user,
            "projects.view_project",
            Project.objects.all(),
        )
        allowed_ids = [cast("Project", p).id for p in allowed_projects]
        return Project.objects.filter(id__in=allowed_ids)


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ProjectSelectionView(
    LoginRequiredMixin,
    ProjectPermissionRequiredMixin,
    ProjectContextMixin,
    TemplateView,
):
    """Handle project selection with object-level permission checks."""

    template_name: str = "projects/projects_selector.html"

    @beartype
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add user's projects to the context using guardian permissions.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Context dictionary for the template.

        """
        context = super().get_context_data(**kwargs)
        user_projects = get_objects_for_user(
            self.request.user,
            "projects.view_project",
            Project.objects.all(),
        )
        context["object_list"] = user_projects
        context["user_projects"] = user_projects
        if self.request.GET.get("project_id"):
            context["selected_project_id"] = self.request.GET.get("project_id")
        return context

    @beartype
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests for project selection.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse for the project selection page.

        """
        return super().get(request, *args, **kwargs)

    @beartype
    def requires_special_access(self, project_id: str, _user: AbstractUser) -> bool:
        """Check if a project requires special access permissions.

        Args:
            project_id: The project ID to check.
            _user: The user to check permissions for.

        Returns:
            True if special access is required, False otherwise.

        """
        try:
            Project.objects.get(id=project_id)
            # Implement your permission logic here
            return False  # Return True if special access is required
        except Project.DoesNotExist:
            logger.warning("Project %s not found during permission check", project_id)
            return False


@beartype
def project_obligations(_request: HttpRequest, project_id: str) -> JsonResponse:
    """Retrieve obligations associated with a specific project.

    Args:
        _request: The HTTP request object.
        project_id: The project ID.

    Returns:
        JsonResponse with obligations data.

    """
    project = get_object_or_404(Project, id=project_id)
    obligations = Obligation.objects.filter(project=project)

    obligations_data = [
        {"id": o.obligation_number, "obligation_number": o.obligation_number}
        for o in obligations
    ]

    return JsonResponse({"obligations": obligations_data})


@beartype
def get_user_role(project: Project, user: AbstractUser) -> str:
    """Get user's role in project.

    Args:
        project: The project to check.
        user: The user to get role for.

    Returns:
        User's role or 'viewer' if none found.

    """
    try:
        return project.get_user_role(user)
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.exception("Error getting user role: %s", e)
        return "viewer"


@beartype
def get_item(dictionary: dict, key: Any) -> Any:
    """Get item from dictionary by key.

    Args:
        dictionary: The dictionary to search.
        key: The key to look up.

    Returns:
        The value for the key, or None if not found.

    """
    return dictionary.get(key)


@beartype
def apply_to_all(queryset: Any, method_name: str) -> list:
    """Call a method on each object in the queryset and return a list of results.

    Args:
        queryset: The queryset of objects.
        method_name: The method name to call on each object.

    Returns:
        List of results from calling the method.

    """
    if method_name == "to_dict":
        return [{"id": str(obj.id), "name": obj.name} for obj in queryset]
    return [getattr(obj, method_name)() for obj in queryset]


@beartype
def format_role(role: str) -> str:
    """Format role name for display.

    Args:
        role: The role string.

    Returns:
        Formatted role string.

    """
    return role.replace("_", " ").title()


@beartype
def role_badge(role: str) -> dict:
    """Render role badge.

    Args:
        role: The role string.

    Returns:
        Dictionary with role, color, and icon.

    """
    colors = {
        "owner": "primary",
        "manager": "success",
        "member": "info",
        "viewer": "secondary",
    }
    badge_icon = {
        "owner": "star",
        "manager": "cog",
        "member": "user",
        "viewer": "eye",
    }
    return {
        "role": role,
        "color": colors.get(role, "secondary"),
        "icon": badge_icon.get(role, ""),
    }


@beartype
def obligation_table(obligations_list: list) -> dict:
    """Render obligation list table.

    Args:
        obligations_list: List of obligations.

    Returns:
        Dictionary with obligations.

    """
    return {"obligations": obligations_list}


@beartype
def get_project(project_id: str) -> Project:
    """Get project by ID.

    Args:
        project_id: The project ID.

    Returns:
        The Project instance.

    """
    return get_object_or_404(Project, id=project_id)


@beartype
def get_user(user_id: str) -> AbstractUser:
    """Get user by ID.

    Args:
        user_id: The user ID.

    Returns:
        The AbstractUser instance.

    """
    return cast("AbstractUser", get_object_or_404(User, id=user_id))


@beartype
@login_required
def export_project(request: HttpRequest, project_id: int) -> HttpResponse:
    """Export a single project as Protocol Buffer binary data.

    Args:
        request: The HTTP request object.
        project_id: The project ID.

    Returns:
        HttpResponse with the exported data or error.

    """
    project = get_object_or_404(Project, id=project_id)
    serializer = ProjectProtoSerializer(instance=project)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export project.")
        return HttpResponse(status=400)
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = f'attachment; filename="project_{project_id}.pb"'
    return response


@beartype
@login_required
def export_all_projects(request: HttpRequest) -> HttpResponse:
    """Export all projects as a Protocol Buffer collection.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse with the exported data or error.

    """
    projects = list(Project.objects.all())
    serializer = ProjectCollectionProtoSerializer(instances=projects)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export projects.")
        return HttpResponse(status=400)
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="projects.pb"'
    return response


@beartype
@login_required
@require_http_methods(["GET", "POST"])
def import_project(request: HttpRequest) -> HttpResponse:
    """Import a project from Protocol Buffer binary data.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse for the import page or result.

    """
    if request.method == "POST":
        if "file" not in request.FILES:
            messages.error(request, "No file was provided.")
            return HttpResponse(status=400)
        uploaded_file = request.FILES["file"]
        try:
            data = uploaded_file.read()
            serializer = ProjectProtoSerializer(data=data)
            if not serializer.is_valid():
                messages.error(
                    request,
                    "Could not deserialize the file. Invalid format.",
                )
                return HttpResponse(status=400)
            project = serializer.validated_data
            project.id = None  # Ensure a new record is created
            project.save()
            messages.success(request, "Project imported successfully.")
            return HttpResponse(status=200)
        except (ValueError, OSError, AttributeError, TypeError) as e:
            logger.exception("Error importing project: %s", e)
            messages.error(request, "An error occurred while importing the project.")
            return HttpResponse(status=400)
    return HttpResponse("Import Project Form")


@beartype
@login_required
def export_project_membership(request: HttpRequest, membership_id: int) -> HttpResponse:
    """Export a single ProjectMembership as Protocol Buffer binary data."""
    membership = get_object_or_404(ProjectMembership, pk=membership_id)
    serializer = ProjectMembershipProtoSerializer(instance=membership)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export project membership.")
        return HttpResponse(status=400)
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = (
        f'attachment; filename="membership_{membership_id}.pb"'
    )
    return response


@beartype
@login_required
def export_all_project_memberships(request: HttpRequest) -> HttpResponse:
    """Export all ProjectMemberships as Protocol Buffer binary data (collection)."""
    memberships = list(ProjectMembership.objects.all())
    from . import projects_pb2  # type: ignore[import]

    # type: ignore[attr-defined]
    collection = projects_pb2.ProjectMembershipCollection()
    for membership in memberships:
        proto = membership.to_pb()  # type: ignore[attr-defined]
        collection.memberships.append(proto)  # type: ignore[attr-defined]
    data = collection.SerializeToString()  # type: ignore[attr-defined]
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="project_memberships.pb"'
    return response


@beartype
@login_required
@require_http_methods(["GET", "POST"])
def import_project_membership(request: HttpRequest) -> HttpResponse:
    """Import a ProjectMembership from Protocol Buffer binary data."""
    if request.method == "POST":
        if "file" not in request.FILES:
            messages.error(request, "No file was provided.")
            return HttpResponse(status=400)
        uploaded_file = request.FILES["file"]
        try:
            data = uploaded_file.read()
            serializer = ProjectMembershipProtoSerializer(data=data)
            if not serializer.is_valid():
                messages.error(
                    request,
                    "Could not deserialize the file. Invalid format.",
                )
                return HttpResponse(status=400)
            membership = serializer.validated_data
            if membership is not None:
                membership.pk = None  # type: ignore[attr-defined]
                membership.save()
                messages.success(request, "Project membership imported successfully.")
                return HttpResponse(status=200)
            messages.error(request, "Deserialized membership is None.")
            return HttpResponse(status=400)
        except (ValueError, OSError, AttributeError, TypeError) as e:
            logger.exception("Error importing project membership: %s", e)
            messages.error(
                request,
                "An error occurred while importing the project membership.",
            )
            return HttpResponse(status=400)
    return HttpResponse("Import ProjectMembership Form")


@beartype
def create_project_with_permissions(user: Any, form: Any) -> Project:
    """Create a project and assign object-level permissions to the creator.

    Args:
        user: The user creating the project.
        form: The validated ProjectForm instance.

    Returns:
        The created Project instance.

    """
    project = form.save(commit=False)
    project.save()
    form.save_m2m()
    assign_perm("view_project", user, project)
    assign_perm("change_project", user, project)
    assign_perm("delete_project", user, project)
    assign_perm("manage_members", user, project)
    return project
