from typing import Any, Union, Optional
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
import logging
from obligations.utils import ObligationAnalyticsProcessor
from obligations.models import Obligation
from .exceptions import ChartDataError
from .error_handlers import handle_error
from .permissions import ProjectPermissionMixin
from .messages import NO_DATA_AVAILABLE, CHART_DATA_UPDATED

logger = logging.getLogger(__name__)


class MechanismDataViewSet(ProjectPermissionMixin, LoginRequiredMixin, View):
    """Handle mechanism-related data requests with analytics processing."""

    processor_class = ObligationAnalyticsProcessor

    @method_decorator(handle_error)
    def dispatch(self, request: Any, *args: Any, **kwargs: Any) -> HttpResponse:
        """Override dispatch to add error handling."""
        return super().dispatch(request, *args, **kwargs)

    def is_htmx_request(self, request: Any) -> bool:
        """Check if request is coming from HTMX."""
        return request.headers.get('HX-Request') == 'true'

    def get_processor(self, project_id: Optional[str] = None) -> ObligationAnalyticsProcessor:
        """Get configured analytics processor instance."""
        queryset = Obligation.objects.all()
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return self.processor_class(queryset)

    def get(self, request: Any) -> Union[JsonResponse, HttpResponse]:
        """Handle GET requests for mechanism data."""
        if not self.has_project_permission(request, **request.GET.dict()):
            return JsonResponse({'error': 'Permission denied'}, status=403)

        project_id = request.GET.get('project')
        mechanism_id = request.GET.get('mechanism')

        try:
            processor = self.get_processor(project_id)
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
