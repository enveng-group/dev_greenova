from typing import Dict, Any, cast, TypeVar, List, Sequence
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from .models import Project
import logging
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseBase  # Changed import
from django.shortcuts import get_object_or_404
from utils.error_handlers import handle_error
from utils.serializers import ChartDataSerializer
from utils.data_utils import BaseAnalyticsProcessor
from utils.mixins import ProjectContextMixin
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.db.models import QuerySet
from obligations.models import Obligation
from obligations.utils import ObligationAnalyticsProcessor
from utils.response_handler import response_handler  # Add this import

User = get_user_model()
logger = logging.getLogger(__name__)

T = TypeVar('T')

def trigger_client_event(response: HttpResponse, event_name: str) -> None:
    """Add HX-Trigger header for client-side events."""
    response_handler.set_htmx_trigger(response, event_name)


class ProjectSelectionView(LoginRequiredMixin, TemplateView):
    """Handle project selection."""
    template_name = 'projects/projects_selector.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests with HTMX support."""
        htmx = getattr(request, 'htmx', None)
        if (htmx):
            context = self.get_context_data(**kwargs)
            response = HttpResponse(
                self._render_template(
                    'projects/partials/project_content.html',
                    context
                )
            )
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
                    str(project.pk): project.get_user_role(user)
                    for project in projects
                }
            })

        except Exception as e:
            logger.error(f"Error getting project data: {str(e)}")
            context['error'] = "Unable to load projects"

        return context

    def _render_template(self, template: str, context: Dict[str, Any]) -> str:
        """Helper method to render template strings."""
        return render_to_string(template, context, request=self.request)


@method_decorator(handle_error, name='dispatch')
class ProjectContentView(LoginRequiredMixin, ProjectContextMixin, TemplateView):
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

                # Get unique mechanisms for this project
                mechanisms: List[str] = list(  # Convert to List[str]
                    project.obligations.values_list(
                        'primary_environmental_mechanism',
                        flat=True
                    )
                    .distinct()
                    .order_by('primary_environmental_mechanism')
                )

                context.update({
                    'project': project,
                    'user_role': project.get_user_role(user),
                    'mechanisms': mechanisms
                })

                # Add chart data for each mechanism
                obligations = cast(QuerySet[Obligation], project.obligations.all())
                processor = ObligationAnalyticsProcessor(obligations)
                chart_data: Dict[str, Dict[str, Any]] = {
                    str(mechanism): ChartDataSerializer.format_mechanism_data([
                        cast(Dict[str, Any], data_point)
                        for data_point in processor.get_mechanism_data(mechanism)['data']
                    ])
                    for mechanism in mechanisms
                }
                context['chart_data'] = chart_data

        except Exception as e:
            logger.error(f"Error getting project content: {str(e)}")
            context['error'] = "Unable to load project content"

        return context
