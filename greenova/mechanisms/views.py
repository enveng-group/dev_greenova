import base64
import io
import logging

import matplotlib
import matplotlib.pyplot as plt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from projects.models import Project

from .figures import get_mechanism_chart, get_overall_chart
from .models import EnvironmentalMechanism

matplotlib.use('Agg')  # Use Agg backend for non-interactive plotting

logger = logging.getLogger(__name__)

@method_decorator(cache_control(max_age=300), name='dispatch')
@method_decorator(vary_on_headers('HX-Request'), name='dispatch')
class MechanismChartView(LoginRequiredMixin, TemplateView):
    template_name = 'mechanisms/mechanism_charts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get('project_id')

        if not project_id or project_id < '1':
            context['error'] = 'No project selected'
            return context

        try:
            # Check if project exists
            project = Project.objects.get(id=project_id)

            # Get mechanisms for this project
            mechanisms = EnvironmentalMechanism.objects.filter(project_id=project_id)

            # Generate charts for each mechanism
            mechanism_charts = []

            # Add overall chart first
            _, overall_chart_data = get_overall_chart(project_id)

            mechanism_charts.append({
                'name': 'Overall Status',
                'image_data': overall_chart_data
            })

            # Generate charts for individual mechanisms
            for mechanism in mechanisms:
                _, chart_data = get_mechanism_chart(mechanism.id)

                mechanism_charts.append({
                    'id': mechanism.id,
                    'name': mechanism.name,
                    'image_data': chart_data
                })

            context['mechanism_charts'] = mechanism_charts
            context['project'] = project

            # Add table data with mechanism ID
            context['table_data'] = [
                {
                    'id': m.id,
                    'name': m.name,
                    'not_started': m.not_started_count,
                    'in_progress': m.in_progress_count,
                    'completed': m.completed_count,
                    'overdue': m.overdue_count,
                    'total': m.not_started_count + m.in_progress_count + m.completed_count + m.overdue_count
                } for m in mechanisms
            ]

        except Project.DoesNotExist:
            context['error'] = f'Project with ID {project_id} not found'
        except Exception as e:
            logger.error(f'Error generating mechanism charts: {str(e)}')
            context['error'] = f'Error generating charts: {str(e)}'

        return context
