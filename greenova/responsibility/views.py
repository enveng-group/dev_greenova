import logging

from core.utils.roles import get_responsibility_choices, get_responsibility_display_name
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from obligations.models import Obligation

from .figures import generate_responsibility_chart

logger = logging.getLogger(__name__)

@method_decorator(cache_control(max_age=300), name='dispatch')
@method_decorator(vary_on_headers('HX-Request'), name='dispatch')
class ResponsibilityChartView(LoginRequiredMixin, TemplateView):
    """View for displaying responsibility charts."""
    template_name = 'responsibility/responsibility_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get('project_id')

        if not project_id:
            context['error'] = 'No project selected'
            return context

        try:
            # Get all obligations for this project
            obligations = Obligation.objects.filter(project_id=project_id)

            # Count obligations by responsibility
            responsibility_counts = {}

            for obligation in obligations:
                # Get proper display name for responsibility
                resp_display = get_responsibility_display_name(obligation.responsibility)

                if resp_display not in responsibility_counts:
                    responsibility_counts[resp_display] = 0
                responsibility_counts[resp_display] += 1

            # Generate chart
            chart_data = generate_responsibility_chart(responsibility_counts)
            context['responsibility_data'] = responsibility_counts
            context['chart_data'] = chart_data
            context['project_id'] = project_id

        except Exception as e:
            logger.error(f'Error generating responsibility chart: {str(e)}')
            context['error'] = f'Error generating chart: {str(e)}'

        return context

@require_GET
def get_responsibility_options(request):
    """API endpoint to get responsibility options."""
    choices = get_responsibility_choices()
    options = [{'value': value, 'display': display} for value, display in choices]
    return JsonResponse({'options': options})
