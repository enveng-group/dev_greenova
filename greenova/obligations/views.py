from typing import Dict, Any
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from datetime import timedelta
from .models import Obligation
import logging

logger = logging.getLogger(__name__)

class ObligationSummaryView(LoginRequiredMixin, TemplateView):
    """View for obligations summary and table."""
    template_name = 'obligations/components/_obligations_summary.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET request."""
        response = super().get(request, *args, **kwargs)
        if request.headers.get('HX-Request'):
            response['HX-Trigger'] = 'obligationsLoaded'
        return response

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Get context data for template."""
        context = super().get_context_data(**kwargs)

        # Try both project_id and project parameters
        project_id = (
            self.request.GET.get('project_id') or
            self.request.GET.get('project')
        )

        logger.debug(f"Request GET params: {self.request.GET}")
        logger.debug(f"Looking for project_id: {project_id}")

        if not project_id:
            context['error'] = 'No project selected.'
            return context

        try:
            today = timezone.now().date()

            # Get all obligations for project with select_related for optimization
            obligations = Obligation.objects.filter(
                project_id=project_id
            ).select_related(
                'project',
                'primary_environmental_mechanism'
            )

            # Calculate summary stats
            context['summary'] = {
                'overdue': obligations.filter(
                    action_due_date__lt=today,
                    status__in=['not started', 'in progress']
                ).count(),
                'due_7days': obligations.filter(
                    action_due_date__range=[today, today + timedelta(days=7)]
                ).count(),
                'due_14days': obligations.filter(
                    action_due_date__range=[today, today + timedelta(days=14)]
                ).count(),
                'due_30days': obligations.filter(
                    action_due_date__range=[today, today + timedelta(days=30)]
                ).count(),
            }

            # Get table data
            context['obligations'] = obligations.order_by('action_due_date')
            context['project_id'] = project_id

            logger.info(
                f"Found {obligations.count()} obligations for project {project_id}"
            )

        except Exception as e:
            logger.error(f"Error loading obligations for project {project_id}: {e}")
            context['error'] = f'Error loading obligations: {str(e)}'

        return context
