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

from .figures import get_procedure_charts as get_all_procedure_charts

matplotlib.use('Agg')  # Use Agg backend for non-interactive plotting
logger = logging.getLogger(__name__)

@method_decorator(cache_control(max_age=300), name='dispatch')
@method_decorator(vary_on_headers('HX-Request'), name='dispatch')
class ProcedureChartsView(LoginRequiredMixin, TemplateView):
    """View for displaying procedure charts filtered by environmental mechanism."""
    template_name = 'procedures/procedure_charts.html'  # Changed to HTML

    def get_template_names(self):
        """Return appropriate template based on request type."""
        if self.request.htmx:
            return [
                'procedures/components/_procedure_charts.html'
            ]  # Changed to HTML
        return [self.template_name]

    def _get_mechanism_and_obligations(self, mechanism_id):
        """Get mechanism and obligations for the given mechanism ID."""
        mechanism = get_object_or_404(EnvironmentalMechanism, id=mechanism_id)
        query = Obligation.objects
        query = query.filter(primary_environmental_mechanism_id=mechanism_id)
        all_obligations = query
        return mechanism, all_obligations

    def _apply_filters(self, obligations, request_params):
        """Apply filters to obligations based on request parameters."""
        filtered_obligations = obligations
        phase_filter = request_params.get('phase', '')
        responsibility_filter = request_params.get('responsibility', '')
        status_filter = request_params.get('status', '')
        look_ahead = request_params.get('lookahead', '') == '14days'
        overdue_only = request_params.get('overdue', '') == 'true'

        if phase_filter:
            filtered_obligations = filtered_obligations.filter(
                project_phase=phase_filter
            )

        if responsibility_filter:
            filtered_obligations = filtered_obligations.filter(
                responsibility=responsibility_filter
            )

        if status_filter:
            filtered_obligations = filtered_obligations.filter(
                status=status_filter
            )

        if look_ahead:
            today = timezone.now().date()
            future_date = today + timedelta(days=14)
            filtered_obligations = filtered_obligations.filter(
                action_due_date__gte=today,
                action_due_date__lte=future_date
            )

        if overdue_only:
            today = timezone.now().date()
            filtered_obligations = filtered_obligations.filter(
                action_due_date__lt=today
            ).exclude(status='completed')

        filters_applied = any([
            phase_filter,
            responsibility_filter,
            status_filter,
            look_ahead,
            overdue_only
        ])

        filter_params = {
            'phase_filter': phase_filter,
            'responsibility_filter': responsibility_filter,
            'status_filter': status_filter,
            'look_ahead': look_ahead,
            'overdue_only': overdue_only,
            'filters_applied': filters_applied
        }

        return filtered_obligations, filter_params

    def _calculate_statistics(self, all_obligations):
        """Calculate statistics based on all obligations."""
        total = all_obligations.count()
        completed = all_obligations.filter(status='completed').count()
        remaining = total - completed

        if total > 0:
            completion_percentage = int((completed / total) * 100)
        else:
            completion_percentage = 0

        return {
            'total': total,
            'completed': completed,
            'remaining': remaining,
            'percentage': completion_percentage
        }

    def _get_available_filters(self, all_obligations):
        """Get available filter options from obligations."""
        phases = all_obligations.values_list(
            'project_phase', flat=True
        ).distinct().order_by('project_phase')

        responsibilities = all_obligations.values_list(
            'responsibility', flat=True
        ).distinct().order_by('responsibility')

        status_options = [
            ('not started', 'Not Started'),
            ('in progress', 'In Progress'),
            ('completed', 'Completed')
        ]

        return {
            'phases': phases,
            'responsibilities': responsibilities,
            'status_options': status_options
        }

    def _generate_responsibility_chart(self, mechanism_id, filtered_obligations=None,
                                       filters_applied=False):
        """Generate responsibility chart based on filtered obligations."""
        if filters_applied and filtered_obligations is not None:
            filtered_ids = filtered_obligations.values_list('id', flat=True)
            fig = get_responsibility_chart(
                mechanism_id,
                filtered_ids=filtered_ids
            )
        else:
            fig = get_responsibility_chart(mechanism_id)

        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)

        base64_data = base64.b64encode(buf.getvalue()).decode()
        img_tag = (
            f'<img src="data:image/png;base64,{base64_data}" '
            f'alt="Responsibility Distribution Chart" '
            f'width="600" height="300">'
        )

        return img_tag

    def _generate_procedure_charts(self, mechanism_id, filtered_obligations,
                                   all_obligations, filters_applied):
        """Generate charts for each procedure."""
        procedure_charts = []

        # Get filtered IDs if filters are applied
        filtered_ids = None
        if filters_applied:
            filtered_ids = filtered_obligations.values_list('id', flat=True)

        # Generate charts for each procedure
        charts_dict = get_all_procedure_charts(
            mechanism_id,
            filtered_ids=filtered_ids
        )

        for procedure_name, fig in charts_dict.items():
            # Create procedure chart data
            procedure_data = self._create_procedure_chart_data(
                procedure_name,
                fig,
                filtered_obligations if filters_applied else all_obligations
            )
            procedure_charts.append(procedure_data)

        return procedure_charts

    def _create_procedure_chart_data(
        self, procedure_name, fig, obligations,
        # Removed unused argument 'filters_applied'
    ):
        """Create data for a specific procedure chart."""
        # Create image for this procedure
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)

        base64_data = base64.b64encode(buf.getvalue()).decode()
        chart_img = (
            f'<img src="data:image/png;base64,{base64_data}" '
            f'alt="{procedure_name} Chart" '
            f'width="300" height="250">'
        )

        # Get obligations for this procedure
        proc_obligations = obligations.filter(procedure=procedure_name)

        # Count status types
        status_counts = {
            'not_started': sum(
                1 for o in proc_obligations if o.status == 'not started'
            ),
            'in_progress': sum(
                1 for o in proc_obligations if o.status == 'in progress'
            ),
            'completed': sum(
                1 for o in proc_obligations if o.status == 'completed'
            ),
            'overdue': sum(1 for o in proc_obligations if o.is_overdue)
        }
        status_counts['total'] = (
            status_counts['not_started']
            + status_counts['in_progress']
            + status_counts['completed']
        )
        return {
            'name': procedure_name,
            'chart': chart_img,
            'stats': status_counts
        }

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """Get context data for rendering the template."""
        context = super().get_context_data(**kwargs)

        # Get mechanism ID from kwargs or request
        mechanism_id = self.kwargs.get('mechanism_id')
        if not mechanism_id:
            mechanism_id = self.request.GET.get('mechanism_id')

        if not mechanism_id:
            context['error'] = 'No mechanism selected'
            return context

        try:
            # Get mechanism and obligations
            mechanism, all_obligations = self._get_mechanism_and_obligations(
                mechanism_id
            )
            context['mechanism'] = mechanism

            # Apply filters from request
            filtered_obligations, filter_params = self._apply_filters(
                all_obligations,
                self.request.GET
            )

            # Calculate statistics
            stats = self._calculate_statistics(all_obligations)

            # Get available filter options
            filter_options = self._get_available_filters(all_obligations)

            # Update context with basic data
            context.update({
                'total_obligations': stats['total'],
                'completed_obligations': stats['completed'],
                'remaining_obligations': stats['remaining'],
                'completion_percentage': stats['percentage'],

                # Save filter state for template
                'filter_phase': filter_params['phase_filter'],
                'filter_responsibility': filter_params['responsibility_filter'],
                'filter_status': filter_params['status_filter'],
                'filter_lookahead': filter_params['look_ahead'],
                'filter_overdue': filter_params['overdue_only'],

                # Add available filter options
                'available_phases': filter_options['phases'],
                'available_responsibilities': filter_options['responsibilities'],
                'status_options': filter_options['status_options'],
            })

            # Generate responsibility chart
            responsibility_chart_img = self._generate_responsibility_chart(
                mechanism_id,
                filtered_obligations,
                filter_params['filters_applied']
            )
            context['responsibility_chart'] = responsibility_chart_img

            # Generate procedure charts
            procedure_charts = self._generate_procedure_charts(
                mechanism_id,
                filtered_obligations,
                all_obligations,
                filter_params['filters_applied']
            )
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

        except (EnvironmentalMechanism.DoesNotExist,
                Obligation.DoesNotExist,
                ValueError,
                TypeError) as exc:
            logger.error('Error generating procedure charts: %s', str(exc))
            context['error'] = f'Error generating charts: {str(exc)}'

        return context
