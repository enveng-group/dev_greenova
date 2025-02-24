from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EnvironmentalMechanism
import json

class MechanismChartView(LoginRequiredMixin, TemplateView):
    template_name = 'mechanisms/mechanism_charts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get('project_id')

        if project_id:
            # Get all mechanisms for this project
            mechanisms = EnvironmentalMechanism.objects.filter(project_id=project_id)

            # Prepare data in the format needed for the polar chart
            chart_data = {
                'names': [],  # Mechanism names
                'not_started': [],  # Not started counts
                'in_progress': [],  # In progress counts
                'completed': []  # Completed counts
            }

            for mech in mechanisms:
                chart_data['names'].append(mech.name or mech.primary_environmental_mechanism)
                chart_data['not_started'].append(mech.not_started_count)
                chart_data['in_progress'].append(mech.in_progress_count)
                chart_data['completed'].append(mech.completed_count)

            context.update({
                'mechanisms': mechanisms,
                'chart_data': json.dumps(chart_data)
            })

        return context
