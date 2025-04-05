import logging
from datetime import datetime
from typing import Any, Dict, Optional, TypedDict, cast

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView, View
from django_htmx.http import push_url, trigger_client_event
from obligations.models import Obligation
from projects.models import Project

# Constants for system information
SYSTEM_STATUS = 'operational'  # or fetch from settings/environment
APP_VERSION = '0.0.5'  # or fetch from settings/environment
LAST_UPDATED = datetime.now().date()  # or fetch from settings/environment

logger = logging.getLogger(__name__)


class DashboardContext(TypedDict):
    projects: QuerySet[Project]
    selected_project_id: Optional[str]
    system_status: str
    app_version: str
    last_updated: datetime
    user: AbstractUser
    debug: bool
    error: Optional[str]
    user_roles: Dict[str, str]


@method_decorator(cache_control(max_age=60), name='dispatch')
@method_decorator(vary_on_headers('HX-Request'), name='dispatch')
class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """Main dashboard view."""
    template_name = 'dashboard/dashboard.jinja'
    login_url = 'account_login'
    redirect_field_name = 'next'
    request = None

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        """Initialize view setup."""
        super().setup(request, *args, **kwargs)
        self.request = request

    def get_template_names(self):
        """Return the template name based on request type."""
        if self.request.htmx:
            return ['dashboard/partials/dashboard_content.jinja']
        return [self.template_name]

    def get(self, request, *args, **kwargs):
        """Handle GET requests with enhanced HTMX support."""
        response = super().get(request, *args, **kwargs)

        # If this is an HTMX request, handle history and URL management
        if request.htmx:
            # Push the URL to browser history for navigation
            current_url = request.build_absolute_uri()
            push_url(response, current_url)

            # Trigger dashboard refresh events
            trigger_client_event(response, 'dashboardLoaded')

            # Also trigger project selection if project_id is in the request
            project_id = request.GET.get('project_id')
            if project_id and project_id != '0':
                logger.debug('Triggering projectSelected event with ID: %s', project_id)
                trigger_client_event(response, 'projectSelected', {'id': project_id})

        return response

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Get the context data for template rendering."""
        context = super().get_context_data(**kwargs)

        try:
            user = cast(AbstractUser, self.request.user)

            # Get projects for the current user with prefetch_related
            projects = self.get_projects().prefetch_related('memberships')

            # Build user_roles dictionary
            user_roles = {}
            for project in projects:
                user_roles[str(project.pk)] = project.get_user_role(user)

            # Get selected project_id from query params
            selected_project_id = self.request.GET.get('project_id')

            context.update({
                'projects': projects,
                'selected_project_id': selected_project_id,
                'system_status': SYSTEM_STATUS,
                'app_version': APP_VERSION,
                'last_updated': LAST_UPDATED,
                'user': user,
                'debug': settings.DEBUG,
                'error': None,
                'user_roles': user_roles,
                'show_feedback_link': True,  # Add this to enable the feedback link
            })

            logger.debug(
                'Dashboard context: selected_project_id=%s',
                selected_project_id
            )

        except (AttributeError, ValueError) as e:
            logger.exception('Error in dashboard context: %s', e)
            context['error'] = str(e)

        return context

    def get_projects(self) -> QuerySet[Project]:
        """Get projects for the current user."""
        try:
            user = cast(AbstractUser, self.request.user)
            return Project.objects.filter(members=user).order_by('-created_at')
        except (AttributeError, ValueError) as e:
            logger.exception('Error fetching projects: %s', e)
            return Project.objects.none()


class OverdueCountView(LoginRequiredMixin, View):
    """View for returning count of overdue obligations for HTMX requests."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET requests for overdue count."""
        try:
            # Get selected project_id from query params
            project_id = request.GET.get('project_id')

            # Base query for overdue obligations
            query_filter = {
                'due_date__lt': datetime.now().date(),
                'status__in': ['open', 'in_progress', 'pending']
            }

            # Add project filter if a project is selected
            if project_id and project_id != '0':
                query_filter['project_id'] = project_id

            # Count overdue obligations
            overdue_count = Obligation.objects.filter(**query_filter).count()

            # Create response
            response = HttpResponse(str(overdue_count))

            # Trigger event for high overdue count
            if overdue_count > 5:
                trigger_client_event(
                    response,
                    'highOverdueCount',
                    {'count': overdue_count}
                )

            return response

        except (AttributeError, ValueError) as e:
            logger.exception('Error getting overdue count: %s', e)
            return HttpResponse('0')  # Return 0 in case of error
