import logging
import matplotlib
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from .models import EnvironmentalMechanism
from .figures import get_overall_chart, get_mechanism_chart
from projects.models import Project
import matplotlib.pyplot as plt
import io
import base64

matplotlib.use('Agg')  # Use Agg backend for non-interactive plotting

logger = logging.getLogger(__name__)

@method_decorator(cache_control(max_age=300), name='dispatch')
@method_decorator(vary_on_headers("HX-Request"), name='dispatch')
class MechanismChartView(LoginRequiredMixin, TemplateView):
    template_name = 'mechanisms/mechanism_charts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get('project_id')

        if not project_id:
            context['error'] = "No project selected"
            return context

        try:
            # Check if project exists
            project = Project.objects.get(id=project_id)

            # Get mechanisms for this project
            mechanisms = EnvironmentalMechanism.objects.filter(project_id=project_id)

            # Generate charts for each mechanism
            mechanism_charts = []

            # Add overall chart first
            overall_fig = get_overall_chart(project_id)

            # Convert figure to base64 for embedding in HTML
            buf = io.BytesIO()
            overall_fig.savefig(buf, format='png', bbox_inches='tight')
            buf.seek(0)
            overall_chart_img = f"<img src='data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}' alt='Overall Status Chart'>"

            mechanism_charts.append({
                'name': 'Overall Status',
                'chart': overall_chart_img
            })

            # Generate charts for individual mechanisms
            for mechanism in mechanisms:
                fig = get_mechanism_chart(mechanism.id)

                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches='tight')
                buf.seek(0)
                chart_img = f"<img src='data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}' alt='{mechanism.name} Chart'>"

                mechanism_charts.append({
                    'name': mechanism.name,
                    'chart': chart_img
                })

            context['mechanism_charts'] = mechanism_charts
            context['project'] = project

            # Add table data
            context['table_data'] = [
                {
                    'name': m.name,
                    'not_started': m.not_started_count,
                    'in_progress': m.in_progress_count,
                    'completed': m.completed_count,
                    'overdue': m.overdue_count,
                    'total': m.not_started_count + m.in_progress_count + m.completed_count + m.overdue_count
                } for m in mechanisms
            ]

        except Project.DoesNotExist:
            context['error'] = f"Project with ID {project_id} not found"
        except Exception as e:
            logger.error(f"Error generating mechanism charts: {str(e)}")
            context['error'] = f"Error generating charts: {str(e)}"

        return context
