from typing import Dict, Any, cast
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .models import Project, ProjectMembership
import logging
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from utils.error_handlers import handle_dashboard_error
from utils.serializers import ChartDataSerializer
from utils.data_utils import AnalyticsDataProcessor

User = get_user_model()
logger = logging.getLogger(__name__)

class ProjectSelectionView(LoginRequiredMixin, TemplateView):
    """Handle project selection."""
    template_name = 'projects/projects_selector.html'

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
            projects = Project.objects.filter(members=user)

            context.update({
                'projects': projects,
                'selected_project_id': self.request.GET.get('project_id', ''),
                'user_roles': {
                    project.id: project.get_user_role(user)
                    for project in projects
                }
            })

        except Exception as e:
            logger.error(f"Error getting project data: {str(e)}")
            context['error'] = "Unable to load projects"

        return context

    def render_to_string(self, template: str, context: dict) -> str:
        """Helper method to render template strings."""
        from django.template.loader import render_to_string
        return render_to_string(template, context, request=self.request)

@handle_dashboard_error
class ProjectContentView(LoginRequiredMixin, TemplateView):
    """Handle project content loading."""
    template_name = 'projects/partials/project_content.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Get context data for project content."""
        context = super().get_context_data(**kwargs)

        try:
            project_id = self.request.GET.get('project_id')
            if project_id:
                project = get_object_or_404(Project, pk=project_id)
                user = cast(AbstractUser, self.request.user)

                context.update({
                    'project': project,
                    'user_role': project.get_user_role(user),
                    'analytics': project.get_analytics()
                })

                analytics = AnalyticsDataProcessor(project.obligations.all())
                context['chart_data'] = ChartDataSerializer.format_mechanism_data(
                    analytics.get_mechanism_data()
                )

        except Exception as e:
            logger.error(f"Error getting project content: {str(e)}")
            context['error'] = "Unable to load project content"

        return context
