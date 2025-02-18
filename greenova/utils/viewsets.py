from typing import Any
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .data_utils import AnalyticsDataProcessor
from .serializers import ChartDataSerializer
from obligations.models import Obligation
from datetime import datetime, timedelta

class MechanismDataViewSet(LoginRequiredMixin, View):
    """Handle mechanism-related data requests."""

    def get(self, request: Any) -> JsonResponse:
        mechanism = request.GET.get('mechanism')
        if not mechanism:
            return JsonResponse(
                {'error': 'Mechanism parameter is required'},
                status=400
            )
            
        processor = AnalyticsDataProcessor(Obligation.objects.all())
        data = processor.get_mechanism_data(mechanism)
        serialized = ChartDataSerializer.format_mechanism_data(data)
        
        return JsonResponse(serialized)

class TrendDataViewSet(LoginRequiredMixin, View):
    """Handle trend analysis data requests."""

    def get(self, request: Any, *args: Any, **kwargs: Any) -> JsonResponse:
        days = int(request.GET.get('days', 30))
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        processor = AnalyticsDataProcessor(Obligation.objects.all())
        time_series_data = processor.get_time_series_data(start_date, end_date)
        dict_data = [point.__dict__ for point in time_series_data]
        serialized = ChartDataSerializer.format_trend_data(dict_data)
        
        return JsonResponse(serialized)