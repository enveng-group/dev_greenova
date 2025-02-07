import csv
from datetime import datetime
from io import TextIOWrapper

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import (
    ObligationFilterForm,
    ObligationForm,
    ObligationImportForm,
    ObligationSearchForm,
)
from .models import Obligation


class ObligationListView(LoginRequiredMixin, ListView):
    """Display list of obligations with filtering and search."""

    model = Obligation
    template_name = 'obligations/pages/list.html'
    context_object_name = 'obligations'
    paginate_by = 20

    def get_queryset(self):
        queryset = Obligation.objects.all()
        form = ObligationFilterForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data.get('project_name'):
                queryset = queryset.filter(
                    project_name__icontains=form.cleaned_data['project_name']
                )
            if form.cleaned_data.get('status'):
                queryset = queryset.filter(status=form.cleaned_data['status'])
            if form.cleaned_data.get('responsibility'):
                queryset = queryset.filter(
                    responsibility__icontains=form.cleaned_data[
                        'responsibility'
                    ]
                )
            if form.cleaned_data.get('due_date_from'):
                queryset = queryset.filter(
                    action_due_date__gte=form.cleaned_data['due_date_from']
                )
            if form.cleaned_data.get('due_date_to'):
                queryset = queryset.filter(
                    action_due_date__lte=form.cleaned_data['due_date_to']
                )
            if form.cleaned_data.get('recurring_only'):
                queryset = queryset.filter(recurring_obligation=True)
            if form.cleaned_data.get('inspection_only'):
                queryset = queryset.filter(inspection=True)

        search_form = ObligationSearchForm(self.request.GET)
        if search_form.is_valid() and search_form.cleaned_data.get('q'):
            query = search_form.cleaned_data['q']
            queryset = queryset.filter(
                Q(obligation_number__icontains=query)
                | Q(project_name__icontains=query)
                | Q(obligation__icontains=query)
                | Q(responsibility__icontains=query)
            )

        return queryset.select_related('created_by', 'updated_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ObligationFilterForm(self.request.GET)
        context['search_form'] = ObligationSearchForm(self.request.GET)
        return context


class ObligationDetailView(LoginRequiredMixin, DetailView):
    """Display detailed view of an obligation."""

    model = Obligation
    template_name = 'obligations/pages/detail.html'
    context_object_name = 'obligation'


class ObligationCreateView(LoginRequiredMixin, CreateView):
    """Create a new obligation."""

    model = Obligation
    form_class = ObligationForm
    template_name = 'obligations/pages/create.html'
    success_url = reverse_lazy('obligations:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ObligationUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing obligation."""

    model = Obligation
    form_class = ObligationForm
    template_name = 'obligations/pages/edit.html'
    context_object_name = 'obligation'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


@login_required
def import_obligations(request):
    """Import obligations from CSV file."""
    if request.method == 'POST':
        form = ObligationImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = TextIOWrapper(
                request.FILES['file'].file, encoding='utf-8'
            )
            reader = csv.DictReader(csv_file)

            success_count = 0
            error_count = 0

            for row in reader:
                try:
                    if form.cleaned_data['update_existing']:
                        obligation, created = (
                            Obligation.objects.update_or_create(
                                obligation_number=row['obligation_number'],
                                defaults={
                                    'project_name': row['project_name'],
                                    'primary_environmental_mechanism': row[
                                        'primary_environmental_mechanism'
                                    ],
                                    # Add other fields here
                                },
                            )
                        )
                    else:
                        obligation = Obligation.objects.create(
                            obligation_number=row['obligation_number'],
                            project_name=row['project_name'],
                            primary_environmental_mechanism=row[
                                'primary_environmental_mechanism'
                            ],
                            # Add other fields here
                        )
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    messages.error(
                        request, f"Error on row {reader.line_num}: {str(e)}"
                    )

            messages.success(
                request,
                f"Successfully imported {success_count} obligations. "
                f"Errors: {error_count}",
            )
            return redirect('obligations:list')
    else:
        form = ObligationImportForm()

    return render(request, 'obligations/pages/import.html', {'form': form})
