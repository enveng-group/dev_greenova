import logging
from django.db.models import Q, QuerySet
from typing import Dict, Any
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from .models import Obligation

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
                # Regular status filtering
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
            project_obligations = Obligation.objects.filter(
                project_id=project_id
            ).select_related(
                'project',
                'primary_environmental_mechanism'
            )

            # Get filter options from the current project only
            context['filter_options'] = {
                'status': project_obligations.values_list(
                    'status', flat=True
                ).distinct().order_by('status'),
                'mechanism': project_obligations.values_list(
                    'primary_environmental_mechanism__name', flat=True
                ).distinct().order_by('primary_environmental_mechanism__name'),
                'phase': project_obligations.values_list(
                    'project_phase', flat=True
                ).exclude(project_phase__isnull=True).distinct().order_by('project_phase')
            }

            # Get and apply filters
            filters = self.get_filters()
            obligations = self.apply_filters(project_obligations, filters)

            # Pagination
            page_number = self.request.GET.get('page', 1)
            paginator = Paginator(obligations, self.items_per_page)
            page_obj = paginator.get_page(page_number)

            # Log info about loaded data
            logger.info(
                f"Loaded {page_obj.paginator.count} obligations for project {project_id} "
                f"(page {page_number} of {page_obj.paginator.num_pages})"
            )

            # Update context
            context.update({
                'obligations': page_obj,
                'page_obj': page_obj,
                'project_id': project_id,
                'active_filters': filters,
                'sort_options': [
                    {'field': 'action_due_date', 'label': 'Action Due Date'},
                    {'field': 'status', 'label': 'Status'},
                    {'field': 'obligation_number', 'label': 'ID'},
                ]
            })

        except Exception as e:
            logger.error(f"Error loading obligations for project {project_id}: {e}")
            context['error'] = f'Error loading obligations: {str(e)}'

        return context
