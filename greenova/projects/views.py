import logging
from typing import Any, Dict, List, Tuple, TypeVar, cast

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from django_htmx.http import HttpResponseClientRedirect, trigger_client_event
from obligations.models import Obligation

from .models import Project

User = get_user_model()
logger = logging.getLogger(__name__)

T = TypeVar('T')

@method_decorator(cache_control(max_age=300), name='dispatch')
@method_decorator(vary_on_headers('HX-Request'), name='dispatch')
class ProjectSelectionView(LoginRequiredMixin, TemplateView):
    """Handle project selection."""
    template_name: str = 'projects/projects_selector.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add user's projects to the context."""
        context = super().get_context_data(**kwargs)
        user_projects = Project.objects.filter(members=self.request.user)
        context['object_list'] = user_projects  # Add projects under 'object_list'
        context['user_projects'] = user_projects  # Add projects under 'user_projects'

        # Add selected project ID to context if present in the request
        if self.request.GET.get('project_id'):
            context['selected_project_id'] = self.request.GET.get('project_id')

        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests for project selection."""
        response = super().get(request, *args, **kwargs)

        # If htmx request, add appropriate triggers and handle client-side updates
        if hasattr(request, 'htmx') and request.htmx:
            # Trigger a client event to refresh any project-dependent elements
            trigger_client_event(response, 'projectSelected')

            # If the user is selecting a project that requires special permissions
            project_id = request.GET.get('project_id')
            if project_id and self.requires_special_access(
                project_id, cast(AbstractUser, request.user)
            ):
                return HttpResponseClientRedirect('/permissions-check/')

        return response

    def requires_special_access(self, project_id: str, _user: AbstractUser) -> bool:
        """Check if a project requires special access permissions."""
        try:
            # Removed unused variable to fix linting issue
            Project.objects.get(id=project_id)
            # Implement your permission logic here
            return False  # Return True if special access is required
        except Project.DoesNotExist:
            logger.warning('Project %s not found during permission check', project_id)
            return False

def project_obligations(_request: HttpRequest, project_id: str) -> JsonResponse:
    """Retrieve obligations associated with a specific project."""
    project = get_object_or_404(Project, id=project_id)
    obligations = Obligation.objects.filter(project=project)

    # Serialize obligations
    obligations_data = [
        {'id': o.obligation_number, 'obligation_number': o.obligation_number}
        for o in obligations
    ]

    return JsonResponse({'obligations': obligations_data})

def get_user_role(project: Project, user: AbstractUser) -> str:
    """
    Get user's role in project.

    Args:
        project: The project to check
        user: The user to get role for
    Returns:
        str: User's role or 'viewer' if none found
    """
    try:
        return project.get_user_role(user)
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error('Error getting user role: %s', e)
        return 'viewer'

def get_item(dictionary: dict, key: Any) -> Any:
    """Get item from dictionary by key."""
    return dictionary.get(key)

def apply_to_all(queryset: Any, method_name: str) -> list:
    """Call a method on each object in the queryset and return a list of results."""
    if method_name == 'to_dict':
        return [{'id': str(obj.id), 'name': obj.name} for obj in queryset]
    return [getattr(obj, method_name)() for obj in queryset]

def format_role(role: str) -> str:
    """Format role name for display."""
    return role.replace('_', ' ').title()

def role_badge(role: str) -> dict:
    """Render role badge."""
    colors = {
        'owner': 'primary',
        'manager': 'success',
        'member': 'info',
        'viewer': 'secondary'
    }
    badge_icon = {
        'owner': 'star',
        'manager': 'cog',
        'member': 'user',
        'viewer': 'eye'
    }
    return {
        'role': role,
        'color': colors.get(role, 'secondary'),
        'icon': badge_icon.get(role, '')
    }

def obligation_table(obligations_list: list) -> dict:
    """Render obligation list table."""
    return {'obligations': obligations_list}

def get_project(project_id: str) -> Project:
    """Get project by ID."""
    return get_object_or_404(Project, id=project_id)

def get_user(user_id: str) -> AbstractUser:
    """Get user by ID."""
    return cast(AbstractUser, get_object_or_404(User, id=user_id))

def get_role_display(role_value: str) -> str:
    """Get the display name for a role value."""
    ROLE_DISPLAY_NAMES = {
        'owner': 'Owner',
        'manager': 'Manager',
        'member': 'Member',
        'viewer': 'Viewer'
    }
    return ROLE_DISPLAY_NAMES.get(role_value, role_value.title())

def get_role_color(role_value: str) -> str:
    """Get the display color for a role value."""
    ROLE_COLORS = {
        'owner': 'success',
        'manager': 'primary',
        'member': 'info',
        'viewer': 'default'
    }
    return ROLE_COLORS.get(role_value, 'default')

def get_role_choices() -> List[Tuple[str, str]]:
    """
    Get choices for model field with human-readable display names.

    Returns:
        List[Tuple[str, str]]: List of tuples (role_value, display_name)
    """
    ROLE_DISPLAY_NAMES = {
        'owner': 'Owner',
        'manager': 'Manager',
        'member': 'Member',
        'viewer': 'Viewer'
    }
    return list(ROLE_DISPLAY_NAMES.items())

def get_responsibility_choices() -> List[Tuple[str, str]]:
    """
    Get choices for the responsibility field in Obligation
    model. Uses display names as values for backward compatibility.

    Returns:
        List[Tuple[str, str]]: List of tuples (display_name, display_name)
    """
    # For the responsibility field, both the key and value are the display name
    # This maintains compatibility with existing data
    return [(display_name, display_name) for _, display_name in get_role_choices()
            if display_name not in ['Owner', 'Manager', 'Member', 'Viewer']]

def get_role_from_responsibility(responsibility: str) -> str:
    """
    Convert a responsibility display name to its corresponding role value.

    Args:
        responsibility (str): The display name of the responsibility
    Returns:
        str: The corresponding role value or None if not found
    """
    ROLE_DISPLAY_NAMES = {
        'owner': 'Owner',
        'manager': 'Manager',
        'member': 'Member',
        'viewer': 'Viewer'
    }
    inverse_map = {display: value for value, display in ROLE_DISPLAY_NAMES.items()}
    return inverse_map.get(responsibility)

def get_responsibility_from_role(role: str) -> str:
    """
    Convert a role value to its corresponding responsibility display name.

    Args:
        role (str): The role value
    Returns:
        str: The corresponding responsibility display name or None if not found
    """
    ROLE_DISPLAY_NAMES = {
        'owner': 'Owner',
        'manager': 'Manager',
        'member': 'Member',
        'viewer': 'Viewer'
    }
    return ROLE_DISPLAY_NAMES.get(role)

def get_responsibility_display_name(responsibility: str) -> str:
    """
    Get the display name for a responsibility value.

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
