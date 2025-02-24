from typing import Any, Dict
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from projects.models import Project
from obligations.models import Obligation
import logging

logger = logging.getLogger(__name__)

class ObligationListView(LoginRequiredMixin, TemplateView):
    """View for listing project obligations."""
    template_name = 'obligations/views/obligations.html'
    paginate_by = 20  # Number of items per page

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Get context data including project and obligations."""
        context = super().get_context_data(**kwargs)
        try:
            project = get_object_or_404(Project, id=self.kwargs.get('project_id'))
            obligations: QuerySet[Obligation] = (
                Obligation.objects
                .filter(project=project)
                .select_related('project')
                .order_by('action_due_date')
            )

            # Get unique mechanisms for filter
            mechanisms = (
                obligations
                .values_list('mechanism', flat=True)
                .distinct()
                .order_by('mechanism')
            )

            # Initialize pagination
            paginator = Paginator(obligations, self.paginate_by)
            page_number = int(self.request.GET.get('page', 1))
            page_obj = paginator.get_page(page_number)

            # Filter obligations if status parameter exists
            status = self.request.GET.get('status', '')
            if status:
                obligations = obligations.filter(status=status)

            context.update({
                'page_obj': page_obj,
                'filtered_obligations': obligations,
                'mechanisms': list(mechanisms),
                'project': project
            })

        except Exception as e:
            logger.error(f"Error in ObligationListView: {str(e)}")
            context['error'] = str(e)

        return context

class FilteredObligationsView(LoginRequiredMixin, ListView):
    """View for filtered obligations list."""
    template_name = 'obligations/tables/obligation_list.html'
    context_object_name = 'obligations'

    def dispatch(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Obligation]:
        """Get filtered queryset of obligations."""
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        queryset = Obligation.objects.filter(project=project)

        mechanism = self.request.GET.get('mechanism')
        if mechanism:
            queryset = queryset.filter(mechanism=mechanism)

        return queryset.select_related('project').order_by('action_due_date')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add additional context."""
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('mechanism')
        return context
