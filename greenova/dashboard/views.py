from typing import Dict, Any, cast, Optional, TypedDict
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from projects.models import Project
from utils.constants import SYSTEM_STATUS, APP_VERSION, LAST_UPDATED
from utils.mixins import NavigationMixin
import logging
from django_htmx.http import trigger_client_event

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
    user_roles: Dict[int, str]

class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """Main dashboard view."""
    template_name = 'dashboard/dashboard.html'
    navigation: Optional[NavigationMixin] = None
    
    def get_navigation(self) -> NavigationMixin:
        """Get or create navigation instance."""
        if not self.navigation:
            self.navigation = NavigationMixin()
        return self.navigation

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        """Initialize view setup."""
        super().setup(request, *args, **kwargs)
        nav = self.get_navigation()
        setattr(nav, 'request', request)

    def get_context_data(self, **kwargs: Dict[str, Any]) -> DashboardContext:
        """Get the context data for template rendering."""
        context = cast(DashboardContext, super().get_context_data(**kwargs))
        
        try:
            user = cast(AbstractUser, self.request.user)
            # Use prefetch_related for ManyToMany relationships
            user_projects = Project.objects.filter(
                memberships__user=user
            ).prefetch_related('memberships').distinct()
            
            dashboard_context: DashboardContext = {
                'projects': user_projects,
                'selected_project_id': self.request.GET.get('project_id'),
                'system_status': SYSTEM_STATUS,
                'app_version': APP_VERSION,
                'last_updated': datetime.combine(LAST_UPDATED, datetime.min.time()),
                'debug': settings.DEBUG,
                'error': None,
                'user': user,
                'user_roles': {
                    project.id: project.get_user_role(user)
                    for project in user_projects
                }
            }
            
            context.update(dashboard_context)
            logger.info(f"Found {user_projects.count()} projects for user {user}")
            
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

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests with HTMX support."""
        if hasattr(request, 'htmx') and getattr(request, 'htmx'):
            return self.handle_htmx_request()
        return super().get(request, *args, **kwargs)

    def render_to_string(self, template: str, context: Dict[str, Any]) -> str:
        """Helper method to render template strings."""
        from django.template.loader import render_to_string
        return render_to_string(template, context, request=self.request)

    def handle_htmx_request(self) -> HttpResponse:
        """Handle HTMX-specific requests."""
        try:
            context = self.get_context_data()
            response = HttpResponse(
                self.render_to_string('dashboard/partials/dashboard_content.html', dict(context))
            )
            trigger_client_event(response, 'dashboardUpdate')
            return response
        except Exception as e:
            logger.error(f"HTMX request error: {str(e)}")
            return HttpResponse(
                f'<div role="alert">Error updating dashboard: {str(e)}</div>',
                status=422
            )