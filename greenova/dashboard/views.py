from typing import Any, Dict
from django.views.generic import TemplateView, ListView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.db.models import QuerySet, Count
from projects.models import Project
from django.conf import settings
from datetime import datetime
import logging
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from utils.mixins import LoggedActionMixin, NavigationMixin
from utils.constants import STATUS_CHOICES, STATUS_NOT_STARTED
from utils.exceptions import ChartDataError
from utils.data_utils import AnalyticsDataProcessor
from utils.serializers import ChartDataSerializer

logger = logging.getLogger(__name__)

class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """Main dashboard view."""
    template_name = 'dashboard/views/dashboard.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'projects': Project.objects.all(),
            'system_status': settings.SYSTEM_STATUS,  # Add this
            'app_version': settings.VERSION,          # Add this
            'last_updated': datetime.now()           # Add this
        })
        return context