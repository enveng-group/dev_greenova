from typing import Dict, Any, cast, Optional, TypedDict
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from django.contrib.auth.models import AbstractUser
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django_htmx.http import (
    HttpResponseClientRedirect,
    HttpResponseClientRefresh,
    trigger_client_event,
    push_url,
    reswap,
    retarget
)
from datetime import datetime
from projects.models import Project
from obligations.models import Obligation
import logging

# Constants for system information
SYSTEM_STATUS = "operational"  # or fetch from settings/environment
APP_VERSION = "0.0.4"  # or fetch from settings/environment
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
@method_decorator(vary_on_headers("HX-Request"), name='dispatch')
class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """Main dashboard view."""
    template_name = 'dashboard/dashboard.html'
    login_url = 'account_login'
    redirect_field_name = 'next'

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        """Initialize view setup."""
        super().setup(request, *args, **kwargs)
        self.request = request

    def get_template_names(self):
        if self.request.htmx:
            return ['dashboard/partials/dashboard_content.html']
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
            if project_id:
                trigger_client_event(response, 'projectSelected', {"projectId": project_id})

            # If the dashboard data is stale, force a refresh
            if self._is_data_stale():
                return HttpResponseClientRefresh()

        return response

    def _is_data_stale(self) -> bool:
        """Check if dashboard data is stale and needs refresh."""
        # Implement your staleness check logic here
        return False

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Get the context data for template rendering."""
        context = super().get_context_data(**kwargs)

        try:
            user = cast(AbstractUser, self.request.user)

            # Use prefetch_related for ManyToMany relationships
            user_projects = Project.objects.filter(
                memberships__user=user
            ).prefetch_related('memberships', 'obligations').distinct()

            # Get the selected project ID from query parameters
            selected_project_id = self.request.GET.get('project_id')

            dashboard_context: DashboardContext = {
                'projects': user_projects,
                'selected_project_id': selected_project_id,  # Add this to context explicitly
                'system_status': SYSTEM_STATUS,
                'app_version': APP_VERSION,
                'last_updated': datetime.combine(LAST_UPDATED, datetime.min.time()),
                'debug': settings.DEBUG,
                'error': None,
                'user': user,
                'user_roles': {
                    str(project.pk): project.get_user_role(user)
                    for project in user_projects
                }
            }

            context.update(dashboard_context)
            logger.info(f"Found {user_projects.count()} projects for user {user}")

            # Add analytics data for selected project
            if selected_project_id:
                try:
                    project = user_projects.get(pk=selected_project_id)

                    # Fix the query - use project directly instead of projects field
                    obligations = Obligation.objects.filter(
                        project=project  # Changed from projects=project
                    ).select_related('project')

                except Project.DoesNotExist:
                    logger.error(f"Project not found: {selected_project_id}")
                    context['error'] = "Selected project not found"
                except Exception as e:
                    logger.error(f"Error processing analytics: {str(e)}")
                    context['error'] = "Error processing analytics data"

        except Exception as e:
            logger.error(f"Error loading dashboard: {str(e)}")
            context['error'] = str(e)

        return context

    def get_projects(self) -> QuerySet[Project]:
        """Get projects for the current user."""
        try:
            return Project.objects.prefetch_related(
                'obligations',
                'memberships'
            ).all()
        except Exception as e:
            logger.error(f"Error fetching projects: {str(e)}")
            return Project.objects.none()

    @classmethod
    @method_decorator(cache_control(max_age=30))
    def overdue_count(cls, request):
        """
        Returns the count of overdue obligations as plain text for HTMX to swap into the page.
        This endpoint is designed to be called via hx-get and refreshed periodically.
        """
        try:
            count = Obligation.objects.filter(
                recurring_status='overdue'
            ).count()

            if request.htmx:
                response = render(
                    request,
                    "dashboard/partials/overdue_count.html",
                    {"count": count}
                )
            else:
                response = HttpResponse(str(count))

            # When the count is over a threshold, highlight it by triggering a CSS change
            if count > 5:
                trigger_client_event(response, 'highOverdueCount', params={'count': count})

            return response

        except Exception as e:
            logger.error(f"Error counting overdue items: {str(e)}")
            return HttpResponse("0")

class DashboardProfileView(TemplateView):
    """Profile view."""
    template_name = 'dashboard/profile.html'
    login_url = 'account_login'
    redirect_field_name = 'next'
