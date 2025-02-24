from typing import Dict, Any, Optional
from django.views.generic import View
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from utils.error_handlers import handle_error
from .services import ChartService

import logging

logger = logging.getLogger(__name__)


@method_decorator(handle_error, name='dispatch')
class ChartView(View):
    """Base view for chart generation and configuration."""

    chart_service = ChartService()

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """Handle GET requests for chart data."""
        try:
            chart_type = request.GET.get('type', 'bar')
            chart_data = self.get_chart_data(request)

            if not chart_data:
                return JsonResponse(
                    {'error': 'No data available'},
                    status=404
                )

            config = self.chart_service.get_chart_config(
                chart_type=chart_type,
                data=chart_data
            )

            return JsonResponse(
                config,
                encoder=DjangoJSONEncoder,
                safe=False
            )

        except Exception as e:
            logger.error(f"Chart generation error: {str(e)}")
            return JsonResponse(
                {'error': 'Error generating chart'},
                status=500
            )

    def get_chart_data(self, request) -> Optional[Dict[str, Any]]:
        """
        Override this method in subclasses to provide specific chart data.

        Args:
            request: The HTTP request object

        Returns:
            Dictionary containing chart data or None if no data available
        """
        raise NotImplementedError(
            "Subclasses must implement get_chart_data()"
        )


@method_decorator(handle_error, name='dispatch')
class ChartConfigView(View):
    """View for retrieving chart configuration presets."""

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """Return chart configuration options."""
        try:
            chart_type = request.GET.get('type')
            if not chart_type:
                return JsonResponse(
                    {'error': 'Chart type required'},
                    status=400
                )

            config = ChartService().get_chart_config(
                chart_type=chart_type,
                data={}
            )

            return JsonResponse(config)

        except Exception as e:
            logger.error(f"Chart config error: {str(e)}")
            return JsonResponse(
                {'error': 'Error getting chart configuration'},
                status=500
            )
