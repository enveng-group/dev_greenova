import matplotlib
matplotlib.use('Agg')  # Set backend before importing pyplot
import matplotlib.pyplot as plt
import io
import base64
import logging
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EnvironmentalMechanism

logger = logging.getLogger(__name__)

class MechanismChartView(LoginRequiredMixin, TemplateView):
    template_name = 'mechanisms/mechanism_charts.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if request.headers.get('HX-Request'):
            response['HX-Trigger'] = 'chartsLoaded'
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get('project')

        if not project_id:
            context['error'] = 'No project selected.'
            return context

        try:
            mechanisms = EnvironmentalMechanism.objects.filter(project_id=project_id)
            if not mechanisms.exists():
                context['error'] = 'No mechanisms found for this project.'
                return context

            mechanism_charts = []

            # Generate overall status distribution
            overall_status_data = {
                'Not Started': sum(m.not_started_count for m in mechanisms),
                'In Progress': sum(m.in_progress_count for m in mechanisms),
                'Completed': sum(m.completed_count for m in mechanisms)
            }

            if sum(overall_status_data.values()) > 0:
                plt.figure(figsize=(10, 6))
                try:
                    # Fix: Use format string for autopct
                    wedges, texts, autotexts = plt.pie(
                        overall_status_data.values(),
                        labels=list(overall_status_data.keys()),
                        autopct=lambda pct: f'{pct:.1f}%',
                        colors=['#ff9999', '#66b3ff', '#99ff99']
                    )
                    plt.title('Overall Status Distribution')

                    # Improve text visibility
                    plt.setp(autotexts, size=8, weight="bold")
                    plt.setp(texts, size=8)

                    status_buffer = io.BytesIO()
                    plt.savefig(status_buffer, format='png', bbox_inches='tight', dpi=100)
                    status_buffer.seek(0)
                    overall_status_chart = base64.b64encode(status_buffer.getvalue()).decode()
                finally:
                    plt.close()
            else:
                overall_status_chart = None

            # Generate individual mechanism charts
            for mechanism in mechanisms:
                mech_status_data = {
                    'Not Started': mechanism.not_started_count,
                    'In Progress': mechanism.in_progress_count,
                    'Completed': mechanism.completed_count
                }

                if sum(mech_status_data.values()) > 0:
                    plt.figure(figsize=(8, 6))
                    try:
                        # Fix: Use format string for autopct
                        wedges, texts, autotexts = plt.pie(
                            mech_status_data.values(),
                            labels=list(mech_status_data.keys()),
                            autopct=lambda pct: f'{pct:.1f}%',
                            colors=['#ff9999', '#66b3ff', '#99ff99']
                        )
                        plt.title(f'{mechanism.name or mechanism.primary_environmental_mechanism}')

                        # Improve text visibility
                        plt.setp(autotexts, size=8, weight="bold")
                        plt.setp(texts, size=8)

                        chart_buffer = io.BytesIO()
                        plt.savefig(chart_buffer, format='png', bbox_inches='tight', dpi=100)
                        chart_buffer.seek(0)
                        chart_data = base64.b64encode(chart_buffer.getvalue()).decode()

                        mechanism_charts.append({
                            'name': mechanism.name or mechanism.primary_environmental_mechanism,
                            'chart': chart_data,
                            'stats': mech_status_data
                        })
                    finally:
                        plt.close()

            # Prepare table data
            table_data = [{
                'name': m.name or m.primary_environmental_mechanism,
                'project': m.project.name,
                'not_started': m.not_started_count,
                'in_progress': m.in_progress_count,
                'completed': m.completed_count,
                'total': m.not_started_count + m.in_progress_count + m.completed_count
            } for m in mechanisms]

            # Modify the data structure to include overall chart in mechanism_charts
            if overall_status_chart:
                mechanism_charts.insert(0, {
                    'name': 'Overall Status',
                    'chart': overall_status_chart,
                    'stats': overall_status_data,
                    'is_overall': True
                })

            context.update({
                'mechanisms': mechanisms,
                'mechanism_charts': mechanism_charts,
                'table_data': table_data,
                'has_charts': bool(mechanism_charts)  # Add this flag
            })

        except Exception as e:
            logger.error(f'Error generating charts: {str(e)}')
            context['error'] = f'Error loading charts: {str(e)}'
            plt.close('all')  # Ensure all figures are closed on error

        return context
