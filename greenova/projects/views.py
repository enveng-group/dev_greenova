import logging
from typing import Any, TypeVar, cast

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from guardian.shortcuts import assign_perm, get_objects_for_user
from obligations.models import Obligation

from .models import Project
from .serializers import (
    ProjectCollectionProtoSerializer,
    ProjectProtoSerializer,
)

User = get_user_model()
logger = logging.getLogger(__name__)

T = TypeVar("T")


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ProjectSelectionView(LoginRequiredMixin, TemplateView):
    """Handle project selection with object-level permission checks."""

    template_name: str = "projects/projects_selector.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add user's projects to the context using guardian permissions."""
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

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests for project selection."""
        return super().get(request, *args, **kwargs)

    def requires_special_access(self, project_id: str, _user: AbstractUser) -> bool:
        """Check if a project requires special access permissions."""
        try:
            Project.objects.get(id=project_id)
            # Implement your permission logic here
            return False  # Return True if special access is required
        except Project.DoesNotExist:
            logger.warning("Project %s not found during permission check", project_id)
            return False


def project_obligations(_request: HttpRequest, project_id: str) -> JsonResponse:
    """Retrieve obligations associated with a specific project."""
    project = get_object_or_404(Project, id=project_id)
    obligations = Obligation.objects.filter(project=project)

    # Serialize obligations
    obligations_data = [
        {"id": o.obligation_number, "obligation_number": o.obligation_number}
        for o in obligations
    ]

    return JsonResponse({"obligations": obligations_data})


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
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.exception("Error getting user role: %s", e)
        return "viewer"


def get_item(dictionary: dict, key: Any) -> Any:
    """Get item from dictionary by key."""
    return dictionary.get(key)


def apply_to_all(queryset: Any, method_name: str) -> list:
    """Call a method on each object in the queryset and return a list of results."""
    if method_name == "to_dict":
        return [{"id": str(obj.id), "name": obj.name} for obj in queryset]
    return [getattr(obj, method_name)() for obj in queryset]


def format_role(role: str) -> str:
    """Format role name for display."""
    return role.replace("_", " ").title()


def role_badge(role: str) -> dict:
    """Render role badge."""
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


def obligation_table(obligations_list: list) -> dict:
    """Render obligation list table."""
    return {"obligations": obligations_list}


def get_project(project_id: str) -> Project:
    """Get project by ID."""
    return get_object_or_404(Project, id=project_id)


def get_user(user_id: str) -> AbstractUser:
    """Get user by ID."""
    return cast("AbstractUser", get_object_or_404(User, id=user_id))


def get_role_display(role_value: str) -> str:
    """Get the display name for a role value."""
    ROLE_DISPLAY_NAMES = {
        "owner": "Owner",
        "manager": "Manager",
        "member": "Member",
        "viewer": "Viewer",
    }
    return ROLE_DISPLAY_NAMES.get(role_value, role_value.title())


def get_role_color(role_value: str) -> str:
    """Get the display color for a role value."""
    ROLE_COLORS = {
        "owner": "success",
        "manager": "primary",
        "member": "info",
        "viewer": "default",
    }
    return ROLE_COLORS.get(role_value, "default")


def get_role_choices() -> list[tuple[str, str]]:
    """Get choices for model field with human-readable display names.

    Returns:
        List[Tuple[str, str]]: List of tuples (role_value, display_name)

    """
    ROLE_DISPLAY_NAMES = {
        "owner": "Owner",
        "manager": "Manager",
        "member": "Member",
        "viewer": "Viewer",
    }
    return list(ROLE_DISPLAY_NAMES.items())


def get_responsibility_choices() -> list[tuple[str, str]]:
    """Get choices for the responsibility field in Obligation
    model. Uses display names as values for backward compatibility.

    Returns:
        List[Tuple[str, str]]: List of tuples (display_name, display_name)

    """
    # For the responsibility field, both the key and value are the display name
    # This maintains compatibility with existing data
    return [
        (display_name, display_name)
        for _, display_name in get_role_choices()
        if display_name not in {"Owner", "Manager", "Member", "Viewer"}
    ]


def get_role_from_responsibility(responsibility: str) -> str:
    """Convert a responsibility display name to its corresponding role value.

    Args:
        responsibility (str): The display name of the responsibility
    Returns:
        str: The corresponding role value or None if not found

    """
    ROLE_DISPLAY_NAMES = {
        "owner": "Owner",
        "manager": "Manager",
        "member": "Member",
        "viewer": "Viewer",
    }
    inverse_map = {display: value for value, display in ROLE_DISPLAY_NAMES.items()}
    return inverse_map.get(responsibility)


def get_responsibility_from_role(role: str) -> str:
    """Convert a role value to its corresponding responsibility display name.

    Args:
        role (str): The role value
    Returns:
        str: The corresponding responsibility display name or None if not found

    """
    ROLE_DISPLAY_NAMES = {
        "owner": "Owner",
        "manager": "Manager",
        "member": "Member",
        "viewer": "Viewer",
    }
    return ROLE_DISPLAY_NAMES.get(role)


def get_responsibility_display_name(responsibility: str) -> str:
    """Get the display name for a responsibility value.

    Args:
        responsibility (str): The responsibility value or display name
    Returns:
        str: The display name for the responsibility

    """
    # If the responsibility is already a display name, return it
    if responsibility in [display for _, display in get_role_choices()]:
        return responsibility

    # Otherwise, convert to display name using the role mapping
    return get_responsibility_from_role(responsibility)


@login_required
def export_project(request, project_id: int) -> HttpResponse:
    """Export a single project as Protocol Buffer binary data."""
    project = get_object_or_404(Project, id=project_id)
    # Optionally restrict to user's projects
    serializer = ProjectProtoSerializer(instance=project)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export project.")
        return HttpResponse(status=400)
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = f'attachment; filename="project_{project_id}.pb"'
    return response


@login_required
def export_all_projects(request) -> HttpResponse:
    """Export all projects as a Protocol Buffer collection."""
    projects = list(Project.objects.all())
    # Optionally restrict to user's projects
    serializer = ProjectCollectionProtoSerializer(instances=projects)
    data = serializer.data()
    if not data:
        messages.error(request, "Failed to export projects.")
        return HttpResponse(status=400)
    response = HttpResponse(data, content_type="application/octet-stream")
    response["Content-Disposition"] = 'attachment; filename="projects.pb"'
    return response


@login_required
@require_http_methods(["GET", "POST"])
def import_project(request) -> HttpResponse:
    """Import a project from Protocol Buffer binary data."""
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
        except (ValueError, OSError, AttributeError, TypeError):
            messages.error(request, "An error occurred while importing the project.")
            return HttpResponse(status=400)
    # GET request - show import form
    return HttpResponse("Import Project Form")


def create_project_with_permissions(user, form):
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
    # Assign object-level permissions to creator
    assign_perm("view_project", user, project)
    assign_perm("change_project", user, project)
    assign_perm("delete_project", user, project)
    assign_perm("manage_members", user, project)
    return project
