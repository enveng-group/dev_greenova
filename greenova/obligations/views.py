import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .models import Obligation


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'obligations/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        obligations = Obligation.objects.filter(person_email=getattr(user, 'email', '')) if user.is_authenticated else Obligation.objects.none()
        context.update(
            {
                'total_count': obligations.count(),
                'overdue_count': obligations.filter(status='overdue').count(),
                'completed_count': obligations.filter(
                    status='completed'
                ).count(),
                'recent_obligations': obligations.order_by('-created_at')[:5],
            }
        )
        return context


class ObligationListView(LoginRequiredMixin, ListView):
    model = Obligation
    template_name = 'obligations/list.html'
    context_object_name = 'obligations'

    def get_queryset(self):
        return Obligation.objects.filter(person_email=getattr(self.request.user, 'email', ''))


class ObligationDetailView(LoginRequiredMixin, DetailView):
    model = Obligation
    template_name = 'obligations/detail.html'


class ObligationCreateView(LoginRequiredMixin, CreateView):
    model = Obligation
    template_name = 'obligations/form.html'
    fields = '__all__'
    success_url = reverse_lazy('obligations:list')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.person_email = getattr(self.request.user, 'email', '')
        return super().form_valid(form)


class ObligationUpdateView(LoginRequiredMixin, UpdateView):
    model = Obligation
    template_name = 'obligations/form.html'
    fields = '__all__'
    success_url = reverse_lazy('obligations:list')


class ObligationDeleteView(LoginRequiredMixin, DeleteView):
    model = Obligation
    template_name = 'obligations/confirm_delete.html'
    success_url = reverse_lazy('obligations:list')


@login_required
def import_obligations(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        # Add CSV import logic here
        return HttpResponse('Import successful')
    return render(request, 'obligations/import.html')


@login_required
def export_obligations(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="obligations.csv"'

    writer = csv.writer(response)
    fields = [field.name for field in Obligation._meta.fields]
    writer.writerow(fields)

    for obligation in Obligation.objects.filter(
        person_email=request.user.email
    ):
        writer.writerow([getattr(obligation, field) for field in fields])

    return response
