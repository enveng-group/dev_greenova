from .models import Report
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name: str
    context_object_name: str
    def get_queryset(self): ...
