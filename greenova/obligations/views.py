from typing import Dict, Any
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Obligation

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
        project_id = self.request.GET.get('project')

        if not project_id:
            context['error'] = 'No project selected.'
            return context

        try:
            today = timezone.now().date()

            # Get all obligations for project
            obligations = Obligation.objects.filter(project_id=project_id)

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
            context['obligations'] = obligations.select_related(
                'project',
                'primary_environmental_mechanism'
            ).order_by('action_due_date')

        except Exception as e:
            context['error'] = f'Error loading obligations: {str(e)}'

        return context
