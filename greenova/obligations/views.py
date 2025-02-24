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
from .filters import ObligationFilter  # Updated to use local import
from utils.error_handlers import handle_error
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)


class ObligationListView(
        LoggedActionMixin,
        ProjectContextMixin,
        LoginRequiredMixin,
        TemplateView):
    """View for listing project obligations."""
    template_name = 'obligations/views/obligations.html'

    @method_decorator(handle_error)
    def dispatch(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        return super().dispatch(request, *args, **kwargs)

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
                .values_list('primary_environmental_mechanism', flat=True)
                .distinct()
                .order_by('primary_environmental_mechanism')
            )

            # Initialize pagination and filtering
            paginator = ProjectPagination(obligations)
            obligation_filter = ObligationFilter(obligations)

            # Convert page number to int with fallback
            page_number = int(self.request.GET.get('page', 1))

            # Create context updates with explicit typing
            context_updates: Dict[str, Any] = {
                'page_obj': paginator.get_page(page_number),
                'filtered_obligations': obligation_filter.filter_by_status(
                    self.request.GET.get('status', '')
                ),
                'mechanisms': list(mechanisms),
                'project': project
            }

            # Update context
            context.update(context_updates)

        except Exception as e:
            logger.error(f"Error in ObligationListView: {str(e)}")
            context['error'] = str(e)

        return context


class FilteredObligationsView(LoggedActionMixin, LoginRequiredMixin, ListView):
    """View for filtered obligations list."""
    template_name = 'obligations/tables/obligation_list.html'
    context_object_name = 'obligations'

    @method_decorator(handle_error)
    def dispatch(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Obligation]:
        """Get filtered queryset of obligations."""
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        queryset = Obligation.objects.filter(project=project)

        mechanism = self.request.GET.get('mechanism')
        if mechanism:
            queryset = queryset.filter(primary_environmental_mechanism=mechanism)

        return queryset.select_related('project').order_by('action_due_date')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add additional context."""
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('mechanism')
        return context
