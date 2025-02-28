import logging
from django.db.models import Q, QuerySet
from typing import Dict, Any, Union, Optional
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from datetime import timedelta
from .models import Obligation
from .forms import ObligationForm
from projects.models import Project

# Create a logger for this module
logger = logging.getLogger(__name__)

class ObligationSummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'obligations/components/_obligations_summary.html'
    items_per_page = 10

    def get_filters(self) -> Dict[str, Any]:
        """Get active filters from request."""
        return {
            'status': self.request.GET.getlist('status'),
            'mechanism': self.request.GET.getlist('mechanism'),
            'phase': self.request.GET.getlist('phase'),
            'search': self.request.GET.get('search', ''),
            'sort': self.request.GET.get('sort', 'action_due_date'),
            'order': self.request.GET.get('order', 'asc'),
            'date_filter': self.request.GET.get('date_filter', ''),
        }

    def apply_filters(self, queryset: QuerySet[Obligation], filters: Dict[str, Any]) -> QuerySet[Obligation]:
        """Apply filters to queryset."""
        if filters['status']:
            if 'overdue' in filters['status']:
                # Handle overdue status separately since it's not in the database
                today = timezone.now().date()
                status_filters = [s for s in filters['status'] if s != 'overdue']

                # Start with a query for overdue items
                overdue_query = Q(
                    action_due_date__lt=today,
                    status__in=['not started', 'in progress']
                )

                # If there are other statuses, add them as OR conditions
                if status_filters:
                    status_query = Q(status__in=status_filters)
                    queryset = queryset.filter(overdue_query | status_query)
                else:
                    queryset = queryset.filter(overdue_query)
            else:
                queryset = queryset.filter(status__in=filters['status'])

        # Rest of the filter logic remains unchanged
        if filters['mechanism']:
            queryset = queryset.filter(
                primary_environmental_mechanism__name__in=filters['mechanism']
            )

        if filters['phase']:
            queryset = queryset.filter(project_phase__in=filters['phase'])

        if filters['search']:
            queryset = queryset.filter(
                Q(obligation_number__icontains=filters['search']) |
                Q(obligation__icontains=filters['search']) |
                Q(environmental_aspect__icontains=filters['search'])
            )

        # Apply date-based filters
        today = timezone.now().date()
        if filters['date_filter'] == '14day_lookahead':
            fourteen_days_later = today + timedelta(days=14)
            queryset = queryset.filter(
                action_due_date__gte=today,
                action_due_date__lte=fourteen_days_later
            ).exclude(status='completed')
        elif filters['date_filter'] == 'overdue':
            queryset = queryset.filter(
                action_due_date__lt=today
            ).exclude(status='completed')

        # Apply sorting
        order_prefix = '-' if filters['order'] == 'desc' else ''
        queryset = queryset.order_by(f"{order_prefix}{filters['sort']}")

        return queryset

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        project_id = (
            self.request.GET.get('project_id') or
            self.request.GET.get('project')
        )

        if not project_id:
            context['error'] = 'No project selected.'
            return context

        try:
            # Get base queryset filtered by project_id
            obligations = Obligation.objects.filter(project_id=project_id)

            # Apply filters
            filters = self.get_filters()
            filtered_obligations = self.apply_filters(obligations, filters)

            # Paginate the results
            page_number = self.request.GET.get('page', 1)
            paginator = Paginator(filtered_obligations, self.items_per_page)
            page_obj = paginator.get_page(page_number)

            # Add to context
            context.update({
                'obligations': page_obj,
                'page_obj': page_obj,
                'project_id': project_id,
                'active_filters': filters,
                'total_count': obligations.count(),
                'filtered_count': filtered_obligations.count(),
            })

        except Exception as e:
            logger.error(f"Error in ObligationSummaryView: {str(e)}")
            context['error'] = f"An error occurred: {str(e)}"

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
    """View for updating an existing obligation."""
    model = Obligation
    form_class = ObligationForm
    template_name = 'obligations/form/update_obligation.html'
    context_object_name = 'obligation'
    pk_url_kwarg = 'obligation_number'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.object.project
        return kwargs

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
