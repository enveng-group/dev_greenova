import logging
from django.db.models import Q, QuerySet
from typing import Dict, Any, Union, Optional
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from datetime import timedelta
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator
from .models import Obligation, ObligationEvidence
from .forms import ObligationForm, EvidenceUploadForm
from projects.models import Project
from mechanisms.models import EnvironmentalMechanism  # Added missing import
from django.views import View
from django.forms import inlineformset_factory
from django_htmx.http import trigger_client_event
from .utils import is_obligation_overdue  # Add explicit import for is_obligation_overdue
from core.types import HttpRequest  # Use the enhanced HttpRequest with htmx property

# Create a logger for this module
logger = logging.getLogger(__name__)

@method_decorator(cache_control(max_age=300), name='dispatch')
@method_decorator(vary_on_headers("HX-Request"), name='dispatch')
class ObligationSummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'obligations/summary.html'

    def get_template_names(self):
        """Return appropriate template based on request type."""
        if self.request.htmx:
            return ['obligations/components/_obligations_summary.html']
        return [self.template_name]

    def apply_filters(self, queryset: QuerySet, filters: Dict[str, Any]) -> QuerySet:
        """Apply filters to the queryset."""
        # Handle the date filter first (14-day lookahead)
        if filters['date_filter'] == '14days':
            today = timezone.now().date()
            two_weeks = today + timedelta(days=14)
            queryset = queryset.filter(
                action_due_date__gte=today,
                action_due_date__lte=two_weeks
            )

        # Apply status filter
        if filters['status']:
            # Handle the special case of 'overdue' status which isn't in the database
            if 'overdue' in filters['status'] and len(filters['status']) == 1:
                from obligations.utils import is_obligation_overdue
                # Filter for items that are overdue
                filtered_ids = []
                for obligation in queryset:
                    if is_obligation_overdue(obligation):
                        filtered_ids.append(obligation.obligation_number)
                queryset = queryset.filter(obligation_number__in=filtered_ids)
            elif 'overdue' in filters['status'] and len(filters['status']) > 1:
                # Handle mix of 'overdue' and other statuses
                other_statuses = [s for s in filters['status'] if s != 'overdue']
                filtered_ids = []
                for obligation in queryset.filter(status__in=other_statuses):
                    if is_obligation_overdue(obligation):
                        filtered_ids.append(obligation.obligation_number)
                queryset = queryset.filter(
                    Q(status__in=other_statuses) | Q(obligation_number__in=filtered_ids)
                )
            else:
                # Normal status filtering
                queryset = queryset.filter(status__in=filters['status'])

        # Apply mechanism filter if provided
        if filters['mechanism']:
            queryset = queryset.filter(
                primary_environmental_mechanism__id__in=filters['mechanism']
            )

        # Apply phase filter if provided
        if filters['phase']:
            queryset = queryset.filter(project_phase__in=filters['phase'])

        # Apply search if provided
        if filters['search']:
            queryset = queryset.filter(
                Q(obligation_number__icontains=filters['search']) |
                Q(obligation__icontains=filters['search']) |
                Q(supporting_information__icontains=filters['search'])
            )

        return queryset

    def get_filters(self) -> Dict[str, Any]:
        """Extract filters from request."""
        return {
            'status': self.request.GET.getlist('status'),
            'mechanism': self.request.GET.getlist('mechanism'),
            'phase': self.request.GET.getlist('phase'),
            'search': self.request.GET.get('search', ''),
            'sort': self.request.GET.get('sort', 'action_due_date'),
            'order': self.request.GET.get('order', 'asc'),
            'date_filter': self.request.GET.get('date_filter', ''),
        }

    def get_context_data(self, **kwargs):
        """Get context data for the template."""
        context = super().get_context_data(**kwargs)

        project_id = self.request.GET.get('project_id')
        if not project_id:
            context['error'] = "Please select a project"
            return context

        try:
            # Verify project exists
            project = get_object_or_404(Project, id=project_id)

            # Get filters from request
            filters = self.get_filters()

            # Get obligations for this project
            queryset = Obligation.objects.filter(project_id=project_id)

            # Apply filters
            queryset = self.apply_filters(queryset, filters)

            # Sort results
            sort_field = filters['sort']
            if filters['order'] == 'desc':
                sort_field = f"-{sort_field}"
            queryset = queryset.order_by(sort_field)

            # Paginate results
            paginator = Paginator(queryset, 15)
            page_number = self.request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)

            context.update({
                'obligations': page_obj,
                'page_obj': page_obj,
                'project': project,
                'project_id': project_id,
                'filters': filters,
                'total_count': paginator.count,
            })

            context['mechanisms'] = EnvironmentalMechanism.objects.filter(project_id=project_id)
            context['phases'] = Obligation.objects.filter(project_id=project_id).values_list('project_phase', flat=True).distinct()
            context['user_can_edit'] = self.request.user.has_perm('obligations.change_obligation')

        except Exception as e:
            logger.error(f"Error in ObligationSummaryView: {str(e)}")
            context['error'] = f"Error loading obligations: {str(e)}"

        return context


class ObligationCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new obligation."""
    model = Obligation
    form_class = ObligationForm
    template_name = 'obligations/form/new_obligation.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project_id = self.request.GET.get('project_id')
        if project_id:
            try:
                project = Project.objects.get(id=project_id)
                kwargs['project'] = project
            except Project.DoesNotExist:
                pass
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get('project_id')
        if project_id:
            context['project_id'] = project_id
        return context

    def form_valid(self, form):
        try:
            # Save the form
            obligation = form.save()

            # Add success message
            messages.success(self.request, f"Obligation {obligation.obligation_number} created successfully.")

            # Redirect to appropriate page
            if 'project_id' in self.request.GET:
                return redirect(f"{reverse('dashboard:home')}?project_id={self.request.GET['project_id']}")
            return redirect('dashboard:home')

        except Exception as e:
            logger.exception(f"Error in ObligationCreateView: {e}")
            messages.error(self.request, f"Failed to create obligation: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class ObligationDetailView(LoginRequiredMixin, DetailView):
    """View for viewing a single obligation."""
    model = Obligation
    template_name = 'obligations/form/view_obligation.html'
    context_object_name = 'obligation'
    pk_url_kwarg = 'obligation_number'


class ObligationUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing obligation."""
    model = Obligation
    form_class = ObligationForm
    template_name = 'obligations/form/update_obligation.html'
    slug_field = 'obligation_number'
    slug_url_kwarg = 'obligation_number'

    def get_template_names(self):
        if self.request.htmx:
            return ['obligations/form/partial_update_obligation.html']
        return [self.template_name]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.object.project
        return kwargs

    def form_valid(self, form):
        """Process the form submission."""
        response = super().form_valid(form)

        # If this is an HTMX request, return appropriate headers
        if self.request.htmx:
            # Using path-deps to refresh dependent components
            response = HttpResponse("Obligation updated successfully")

            # Explicitly trigger a refresh for path-deps components
            trigger_client_event(response, "path-deps-refresh", {
                "path": "/obligations/"
            })

            return response

        return response

    def form_valid(self, form):
        try:
            old_mechanism = None
            if self.object.primary_environmental_mechanism:
                old_mechanism = self.object.primary_environmental_mechanism

            # Save the updated obligation
            obligation = form.save()

            # Update mechanism counts
            if old_mechanism and old_mechanism != obligation.primary_environmental_mechanism:
                if old_mechanism:
                    old_mechanism.update_obligation_counts()
                if obligation.primary_environmental_mechanism:
                    obligation.primary_environmental_mechanism.update_obligation_counts()
            elif obligation.primary_environmental_mechanism:
                obligation.primary_environmental_mechanism.update_obligation_counts()

            # Add success message
            messages.success(self.request, f"Obligation {obligation.obligation_number} updated successfully.")

            # Redirect back to the appropriate page
            if 'project_id' in self.request.GET:
                return redirect(f"{reverse('dashboard:home')}?project_id={self.request.GET['project_id']}")
            return redirect('dashboard:home')

        except Exception as e:
            logger.exception(f"Error in ObligationUpdateView: {e}")
            messages.error(self.request, f"Failed to update obligation: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class ObligationDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting an obligation."""
    model = Obligation
    pk_url_kwarg = 'obligation_number'

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            project_id = self.object.project_id
            mechanism = self.object.primary_environmental_mechanism

            # Delete the obligation
            self.object.delete()
            logger.info(f"Obligation {kwargs.get('obligation_number')} deleted successfully")

            # Update mechanism counts
            if mechanism:
                mechanism.update_obligation_counts()

            # Return JSON response for AJAX calls
            return JsonResponse({
                "status": "success",
                "message": f"Obligation {kwargs.get('obligation_number')} deleted successfully",
                "redirect_url": f"{reverse('dashboard:home')}?project_id={project_id}"
            })

        except Exception as e:
            logger.error(f"Error deleting obligation: {str(e)}")
            return JsonResponse({
                "status": "error",
                "message": f"Error deleting obligation: {str(e)}"
            }, status=400)

@method_decorator(vary_on_headers("HX-Request"), name='dispatch')
class ToggleCustomAspectView(View):
    def get(self, request):
        aspect = request.GET.get('environmental_aspect')
        if aspect == 'Other':
            return render(request, 'obligations/partials/custom_aspect_field.html', {
                'show_field': True
            })
        return render(request, 'obligations/partials/custom_aspect_field.html', {
            'show_field': False
        })

def upload_evidence(request, obligation_id):
    obligation = get_object_or_404(Obligation, pk=obligation_id)

    # Check if obligation already has 5 files
    if ObligationEvidence.objects.filter(obligation=obligation).count() >= 5:
        messages.error(request, "This obligation already has the maximum of 5 evidence files")
        return redirect('obligation_detail', obligation_id=obligation_id)

    if request.method == 'POST':
        form = EvidenceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            evidence = form.save(commit=False)
            evidence.obligation = obligation
            evidence.save()
            messages.success(request, "Evidence file uploaded successfully")
            return redirect('obligation_detail', obligation_id=obligation_id)
    else:
        form = EvidenceUploadForm()
        return render(request, 'upload_evidence.html', {
            'obligation': obligation,
            'form': form,
        })
