from typing import Any
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from .data_utils import AnalyticsDataProcessor
from .serializers import ChartDataSerializer
from obligations.models import Obligation
from datetime import datetime, timedelta
from django_htmx.http import trigger_client_event

class ChartDataError(Exception):
    pass

class MechanismDataViewSet(LoginRequiredMixin, View):
    """Handle mechanism-related data requests."""

    def get(self, request: Any) -> JsonResponse | HttpResponse:
        mechanism = request.GET.get('mechanism')
        if not mechanism:
            if request.htmx:
                return HttpResponse(
                    '<div class="error">Mechanism parameter is required</div>',
                    status=400
                )
            return JsonResponse({'error': 'Mechanism parameter is required'}, status=400)
            
        try:
            processor = AnalyticsDataProcessor(Obligation.objects.all())
            serialized = processor.get_mechanism_data(mechanism)
            
            if request.htmx:
                response = HttpResponse(
                    render_to_string('components/charts/mechanism_chart.html', 
                    {'chart_data': serialized})
                )
                trigger_client_event(response, 'chartDataUpdated')
                return response
            return JsonResponse(serialized)
        except ChartDataError as e:
            if request.htmx:
                return HttpResponse(
                    f'<div class="error">{str(e)}</div>',
                    status=422
                )
            return JsonResponse({'error': str(e)}, status=422)


class TrendDataViewSet(LoginRequiredMixin, View):
    """Handle trend analysis data requests."""

    def get(self, request: Any) -> JsonResponse:
        days = int(request.GET.get('days', 30))
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        processor = AnalyticsDataProcessor(Obligation.objects.all())
        time_series_data = processor.get_time_series_data(start_date, end_date)
        dict_data = [point.__dict__ for point in time_series_data]
        serialized = ChartDataSerializer.format_trend_data(dict_data)
        
        return JsonResponse(serialized)