from typing import Any, Dict
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from projects.models import Project
from obligations.models import Obligation
from utils.mixins import LoggedActionMixin, ProjectContextMixin
import logging
from utils.pagination import ProjectPagination
from utils.filters import ObligationFilter
from utils.error_handlers import handle_dashboard_error

logger = logging.getLogger(__name__)

@handle_dashboard_error
class ObligationListView(LoggedActionMixin, ProjectContextMixin, LoginRequiredMixin, TemplateView):
    """View for listing project obligations.

    Note: Order of inheritance is important for proper MRO:
    1. LoggedActionMixin (provides logging functionality)
    2. ProjectContextMixin (provides project context)
    3. LoginRequiredMixin (provides authentication)
    4. TemplateView (base view class)
    """
    template_name = 'obligations/views/obligations.html'

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Get context data including project and obligations."""
        context = super().get_context_data(**kwargs)
        try:
            project = get_object_or_404(Project, id=self.kwargs.get('project_id'))
            obligations = (
                Obligation.objects
                .filter(project=project)
                .select_related('project')
                .order_by('action_due_date')
            )

            # Get unique mechanisms for filter
            mechanisms = (
                obligations
                .values_list('primary_environmental_mechanism', flat=True)
                .distinct()
                .order_by('primary_environmental_mechanism')
            )

            paginator = ProjectPagination(self.get_queryset())
            obligation_filter = ObligationFilter(self.get_queryset())
            context['page_obj'] = paginator.get_page(self.request.GET.get('page', 1))
            context['filtered_obligations'] = obligation_filter.filter_by_status(
                self.request.GET.get('status', '')
            )

            context.update({
                'project': project,
                'obligations': obligations,
                'mechanisms': mechanisms,
                'current_filter': None
            })

        except Exception as e:
            logger.error(f"Error in ObligationListView: {str(e)}")
            context['error'] = "Error loading obligations"

        return context

class FilteredObligationsView(LoggedActionMixin, LoginRequiredMixin, ListView):
    """View for filtered obligations list.

    Note: Order of inheritance follows same pattern as above
    """
    template_name = 'obligations/tables/obligation_list.html'
    context_object_name = 'obligations'

    def get_queryset(self) -> QuerySet[Obligation]:
        """Get filtered queryset of obligations."""
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        queryset = Obligation.objects.filter(project=project)












        return context        context['current_filter'] = self.request.GET.get('mechanism')        context = super().get_context_data(**kwargs)        """Add additional context."""    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:        return queryset.select_related('project').order_by('action_due_date')                        queryset = queryset.filter(primary_environmental_mechanism=mechanism)        if mechanism:        mechanism = self.request.GET.get('mechanism')
