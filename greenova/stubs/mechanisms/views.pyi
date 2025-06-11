from .figures import get_mechanism_chart as get_mechanism_chart, get_overall_chart as get_overall_chart
from .models import EnvironmentalMechanism
from _typeshed import Incomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from obligations.models import Obligation as Obligation

logger: Incomplete

class MechanismChartView(LoginRequiredMixin, TemplateView):
    template_name: str
    def get_context_data(self, **kwargs): ...

class MechanismListView(LoginRequiredMixin, ListView):
    model = EnvironmentalMechanism
    template_name: str
    context_object_name: str
    def get_queryset(self): ...

def mechanism_chart_data_json(request): ...
