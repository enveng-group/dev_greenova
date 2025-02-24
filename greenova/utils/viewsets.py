from typing import Any, Union
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
import logging
from .data_utils import AnalyticsDataProcessor
from obligations.models import Obligation
from .exceptions import ChartDataError
from .error_handlers import handle_dashboard_error
from .permissions import ProjectPermissionMixin
from .messages import NO_DATA_AVAILABLE, CHART_DATA_UPDATED

logger = logging.getLogger(__name__)

@handle_dashboard_error
class MechanismDataViewSet(ProjectPermissionMixin, LoginRequiredMixin, View):
    """Handle mechanism-related data requests."""

    def is_htmx_request(self, request: Any) -> bool:
        return request.headers.get('HX-Request') == 'true'

    def get(self, request: Any) -> Union[JsonResponse, HttpResponse]:
        """Handle GET requests for mechanism data."""
        if not self.has_project_permission(request, **request.GET.dict()):
            return JsonResponse({'error': 'Permission denied'}, status=403)

        project_id = request.GET.get('project')
        mechanism_id = request.GET.get('mechanism')

        try:
            processor = AnalyticsDataProcessor(
                Obligation.objects.all(),
                project_id=project_id if project_id else None
            )
            data = processor.get_mechanism_data(mechanism_id or "all")

            if not data['data']:
                return JsonResponse({'message': NO_DATA_AVAILABLE}, status=204)

            if self.is_htmx_request(request):
                return HttpResponse(
                    render_to_string(
                        'mechanisms/partials/chart_data.html',
                        {'data': data, 'message': CHART_DATA_UPDATED}
                    )
                )
            return JsonResponse(data)

        except ChartDataError as e:
            logger.error(f"Chart data error: {e}")
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse(
                {'error': 'An unexpected error occurred'},
                status=500
            )
