import base64
import io
import logging
from datetime import timedelta
from typing import Any, Dict

import matplotlib
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from mechanisms.models import EnvironmentalMechanism
from obligations.models import Obligation
from responsibility.figures import get_responsibility_chart

from .figures import get_all_procedure_charts

matplotlib.use('Agg')  # Use Agg backend for non-interactive plotting
logger = logging.getLogger(__name__)

@method_decorator(cache_control(max_age=300), name='dispatch')
@method_decorator(vary_on_headers('HX-Request'), name='dispatch')
class ProcedureChartsView(LoginRequiredMixin, TemplateView):
    """View for displaying procedure charts filtered by environmental mechanism."""
    template_name = 'procedures/procedure_charts.html'

    def get_template_names(self):
        """Return appropriate template based on request type."""
        if self.request.htmx:
            return ['procedures/components/_procedure_charts.html']
        return [self.template_name]

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """Get context data for rendering the template."""
        context = super().get_context_data(**kwargs)
        mechanism_id = self.kwargs.get('mechanism_id') or self.request.GET.get('mechanism_id')

        if not mechanism_id:
            context['error'] = 'No mechanism selected'
            return context

        try:
            # Get the mechanism
            mechanism = get_object_or_404(EnvironmentalMechanism, id=mechanism_id)
            context['mechanism'] = mechanism

            # Get all obligations for this mechanism for filtering
            all_obligations = Obligation.objects.filter(primary_environmental_mechanism_id=mechanism_id)

            # Get filter parameters from request
            phase_filter = self.request.GET.get('phase', '')
            responsibility_filter = self.request.GET.get('responsibility', '')
            status_filter = self.request.GET.get('status', '')
            look_ahead = self.request.GET.get('lookahead', '') == '14days'
            overdue_only = self.request.GET.get('overdue', '') == 'true'

            # Apply filters
            filtered_obligations = all_obligations

            if phase_filter:
                filtered_obligations = filtered_obligations.filter(project_phase=phase_filter)

            if responsibility_filter:
                filtered_obligations = filtered_obligations.filter(responsibility=responsibility_filter)

            if status_filter:
                filtered_obligations = filtered_obligations.filter(status=status_filter)

            if look_ahead:
                today = timezone.now().date()
                future_date = today + timedelta(days=14)
                filtered_obligations = filtered_obligations.filter(action_due_date__gte=today, action_due_date__lte=future_date)

            if overdue_only:
                today = timezone.now().date()
                filtered_obligations = filtered_obligations.filter(
                    action_due_date__lt=today
                ).exclude(status='completed')

            # Calculate statistics
            total_obligations = all_obligations.count()
            completed_obligations = all_obligations.filter(status='completed').count()
            remaining_obligations = total_obligations - completed_obligations
            completion_percentage = int((completed_obligations / total_obligations) * 100) if total_obligations > 0 else 0

            # Add statistics to context
            context.update({
                'total_obligations': total_obligations,
                'completed_obligations': completed_obligations,
                'remaining_obligations': remaining_obligations,
                'completion_percentage': completion_percentage,

                # Save filter state for template
                'filter_phase': phase_filter,
                'filter_responsibility': responsibility_filter,
                'filter_status': status_filter,
                'filter_lookahead': look_ahead,
                'filter_overdue': overdue_only,

                # Add available filter options
                'available_phases': all_obligations.values_list('project_phase', flat=True).distinct().order_by('project_phase'),
                'available_responsibilities': all_obligations.values_list('responsibility', flat=True).distinct().order_by('responsibility'),
                'status_options': [('not started', 'Not Started'), ('in progress', 'In Progress'), ('completed', 'Completed')],
            })

            # Generate responsibility chart based on filtered obligations if filters are applied
            # or all obligations if no filters
            if any([phase_filter, responsibility_filter, status_filter, look_ahead, overdue_only]):
                # Use filtered obligations for the responsibility chart
                responsibility_fig = get_responsibility_chart(mechanism_id, filtered_ids=filtered_obligations.values_list('id', flat=True))
            else:
                # Use all obligations for the chart
                responsibility_fig = get_responsibility_chart(mechanism_id)

            # Convert responsibility figure to base64 for embedding in HTML
            buf = io.BytesIO()
            responsibility_fig.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            # Fixed image tag with double quotes and width/height attributes
            responsibility_chart_img = f"<img src=\"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}\" alt=\"Responsibility Distribution Chart\" width=\"600\" height=\"300\">"

            # Add responsibility chart to context
            context['responsibility_chart'] = responsibility_chart_img

            # Get procedure charts - either filtered or all
            procedure_charts = []

            # Generate charts for each procedure
            charts_dict = get_all_procedure_charts(
                mechanism_id,
                filtered_ids=filtered_obligations.values_list('id', flat=True) if any([phase_filter, responsibility_filter, status_filter, look_ahead, overdue_only]) else None
            )

            for procedure_name, fig in charts_dict.items():
                # Convert figure to base64 for embedding in HTML
                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches='tight')
                buf.seek(0)
                # Fixed image tag with double quotes and width/height attributes
                chart_img = f"<img src=\"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}\" alt=\"{procedure_name} Chart\" width=\"300\" height=\"250\">"

                # Get obligation counts for this procedure
                if any([phase_filter, responsibility_filter, status_filter, look_ahead, overdue_only]):
                    procedure_obligations = filtered_obligations.filter(procedure=procedure_name)
                else:
                    procedure_obligations = all_obligations.filter(procedure=procedure_name)

                # Count status types
                not_started = sum(1 for o in procedure_obligations if o.status == 'not started')
                in_progress = sum(1 for o in procedure_obligations if o.status == 'in progress')
                completed = sum(1 for o in procedure_obligations if o.status == 'completed')
                overdue = sum(1 for o in procedure_obligations if o.is_overdue)

                procedure_charts.append({
                    'name': procedure_name,
                    'chart': chart_img,
                    'stats': {
                        'not_started': not_started,
                        'in_progress': in_progress,
                        'completed': completed,
                        'overdue': overdue,
                        'total': not_started + in_progress + completed
                    }
                })

            context['procedure_charts'] = procedure_charts

            # Add table data for all procedures
            context['table_data'] = [
                {
                    'name': chart['name'],
                    'not_started': chart['stats']['not_started'],
                    'in_progress': chart['stats']['in_progress'],
                    'completed': chart['stats']['completed'],
                    'overdue': chart['stats']['overdue'],
                    'total': chart['stats']['total']
                } for chart in procedure_charts
            ]

        except Exception as e:
            logger.error(f'Error generating procedure charts: {str(e)}')
            context['error'] = f'Error generating charts: {str(e)}'

        return context
