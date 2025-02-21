from typing import Dict, Any, cast
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .models import Project, ProjectMembership
import logging
from django.http import HttpRequest, HttpResponse

User = get_user_model()
logger = logging.getLogger(__name__)

class ProjectSelectionView(LoginRequiredMixin, TemplateView):
    """Handle project selection."""
    template_name = 'projects/partials/projects.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests with HTMX support."""
        htmx = getattr(request, 'htmx', None)
        if htmx:
            context = self.get_context_data(**kwargs)
            response = HttpResponse(
                self.render_to_string('projects/partials/project_content.html', context)
            )
            # Trigger event for client-side updates
            trigger_client_event(response, 'projectSelected')
            return response
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Get context data for project selection."""
        context = super().get_context_data(**kwargs)

        try:
            user = cast(AbstractUser, self.request.user)
            logger.info(f"Getting projects for user ID: {user.pk}")

            # Get projects with efficient querying
            projects = (Project.objects
                      .filter(memberships__user=user)
                      .prefetch_related('memberships', 'obligations')
                      .distinct())

            # Get user roles for each project
            user_roles: Dict[int, str] = {}
            for project in projects:
                try:
                    membership = project.memberships.get(user=user)
                    user_roles[project.id] = membership.role
                except ProjectMembership.DoesNotExist:
                    continue

            context.update({
                'projects': projects,
                'user_roles': user_roles,
                'selected_project_id': self.request.GET.get('project_id'),
                'debug': settings.DEBUG
            })

        except Exception as e:
            logger.error(f"Error in project selection: {str(e)}")
            context['error'] = 'Unable to load projects'

        return context

    def render_to_string(self, template: str, context: dict) -> str:
        """Helper method to render template strings."""
        from django.template.loader import render_to_string
        return render_to_string(template, context, request=self.request)

class ProjectContentView(LoginRequiredMixin, TemplateView):
    """Handle project content loading."""
    template_name = 'projects/partials/project_content.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Get context data for project content."""
        context = super().get_context_data(**kwargs)

        try:
            project = Project.objects.get(id=kwargs['project_id'])
            user = cast(AbstractUser, self.request.user)
            context.update({
                'project': project,
                'user_context': project.get_user_context(user),
                'analytics': project.get_analytics()
            })
        except Project.DoesNotExist:
            context['error'] = 'Project not found'

        return context
