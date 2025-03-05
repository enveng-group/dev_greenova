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

            # Generate overall status distribution - include overdue
            overall_status_data = {
                'Overdue': sum(m.overdue_count for m in mechanisms),
                'Not Started': sum(m.not_started_count for m in mechanisms) - sum(m.overdue_count for m in mechanisms if m.not_started_count > 0),
                'In Progress': sum(m.in_progress_count for m in mechanisms),
                'Completed': sum(m.completed_count for m in mechanisms)
            }

            # Remove categories with zero values
            overall_status_data = {k: v for k, v in overall_status_data.items() if v > 0}

            if sum(overall_status_data.values()) > 0:
                plt.figure(figsize=(10, 6))
                try:
                    # Use appropriate colors including red for overdue
                    colors = {
                        'Overdue': '#ff0000',       # Red for overdue
                        'Not Started': '#ff9999',   # Light red
                        'In Progress': '#66b3ff',   # Blue
                        'Completed': '#99ff99'      # Green
                    }

                    chart_colors = [colors[status] for status in overall_status_data.keys()]

                    # Create the pie chart
                    wedges, texts, autotexts = plt.pie(
                        list(overall_status_data.values()),
                        labels=list(overall_status_data.keys()),
                        autopct=lambda pct: f'{pct:.1f}%' if pct > 5 else '',
                        colors=chart_colors
                    )
                    plt.title('Overall Status Distribution')

                    # Improve text visibility
                    plt.setp(autotexts, size=8, weight="bold")
                    plt.setp(texts, size=8)

                    status_buffer = io.BytesIO()
                    plt.savefig(status_buffer, format='png', bbox_inches='tight', dpi=100)
                    status_buffer.seek(0)

                    overall_status_chart = base64.b64encode(status_buffer.getvalue()).decode('utf-8')
                    plt.close()

                except Exception as e:
                    logger.error(f"Error creating overall chart: {e}")
                    overall_status_chart = None
                    plt.close()
            else:
                overall_status_chart = None

            # Generate individual mechanism charts
            for mechanism in mechanisms:
                # Include overdue in individual charts
                mech_status_data = {
                    'Overdue': mechanism.overdue_count,
                    'Not Started': max(0, mechanism.not_started_count - mechanism.overdue_count),
                    'In Progress': mechanism.in_progress_count,
                    'Completed': mechanism.completed_count
                }

                # Remove categories with zero values
                mech_status_data = {k: v for k, v in mech_status_data.items() if v > 0}

                if sum(mech_status_data.values()) > 0:
                    try:
                        plt.figure(figsize=(7, 5))

                        # Use appropriate colors
                        colors = {
                            'Overdue': '#ff0000',       # Red for overdue
                            'Not Started': '#ff9999',   # Light red
                            'In Progress': '#66b3ff',   # Blue
                            'Completed': '#99ff99'      # Green
                        }

                        chart_colors = [colors[status] for status in mech_status_data.keys()]

                        wedges, texts, autotexts = plt.pie(
                            list(mech_status_data.values()),
                            labels=list(mech_status_data.keys()),
                            autopct=lambda pct: f'{pct:.1f}%' if pct > 5 else '',
                            colors=chart_colors
                        )
                        plt.title(mechanism.name, fontsize=10)

                        plt.setp(autotexts, size=8, weight="bold")
                        plt.setp(texts, size=8)

                        chart_buffer = io.BytesIO()
                        plt.savefig(chart_buffer, format='png', bbox_inches='tight', dpi=100)
                        chart_buffer.seek(0)

                        chart_data = base64.b64encode(chart_buffer.getvalue()).decode('utf-8')
                        plt.close()

                        mechanism_charts.append({
                            'name': mechanism.name,
                            'chart': chart_data,
                            'stats': mech_status_data
                        })

                    except Exception as e:
                        logger.error(f"Error creating chart for {mechanism.name}: {e}")
                        plt.close()

            # Prepare table data - include overdue column
            table_data = [{
                'name': m.name or m.primary_environmental_mechanism,
                'project': m.project.name,
                'overdue': m.overdue_count,
                'not_started': max(0, m.not_started_count - m.overdue_count),
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
                'has_charts': bool(mechanism_charts)
            })
            
            return context
            
        except Exception as e:
            logger.error(f'Error generating charts: {str(e)}')
            context['error'] = f'Error loading charts: {str(e)}'
            plt.close('all')  # Ensure all figures are closed on error
            return context
