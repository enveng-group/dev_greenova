from typing import Any, Dict, List, TypeVar, Generic
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Model
from utils.mixins import LoggedActionMixin
from .actions import AnalyticsActions
from .pagination import ProjectPagination
from .filters import ObligationFilter
from .error_handlers import handle_dashboard_error

T = TypeVar('T', bound=Model)

@handle_dashboard_error
class AnalyticsView(LoggedActionMixin, LoginRequiredMixin, Generic[T], TemplateView):
    """Base view for analytics pages."""

    actions: AnalyticsActions = AnalyticsActions()
    model: type[T]

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add common analytics context data."""
        context = super().get_context_data(**kwargs)
        try:
            queryset = self.get_queryset()

            # Add pagination
            paginator = ProjectPagination(queryset)
            page = self.request.GET.get('page', 1)
            context['page_obj'] = paginator.get_page(page)

            # Add filtering
            if isinstance(queryset.first(), Obligation):
                obligation_filter = ObligationFilter(queryset)
                status = self.request.GET.get('status')
                if status:
                    queryset = obligation_filter.filter_by_status(status)

            context['queryset'] = queryset
            context['metrics'] = self.actions.calculate_metrics(queryset)
            return context
        except Exception as e:
            context['error'] = str(e)
            return context

    def get_chart_config(self) -> Dict[str, Any]:
        """Get chart configuration."""
        return {
            'type': 'doughnut',
            'options': {
                'responsive': True,
                'maintainAspectRatio': True
            }
        }

    def get_mechanisms(self) -> List[str]:
        """Get list of mechanisms."""
        return list(self.get_queryset().values_list(
            'primary_environmental_mechanism',
            flat=True
        ).distinct())

    def get_aspects(self) -> List[str]:
        """Get list of aspects."""
        return list(self.get_queryset().values_list(
            'environmental_aspect',
            flat=True
        ).distinct())

    def get_statuses(self) -> List[str]:
        """Get list of statuses."""


















        return self.model.objects.all()            raise ValueError("Model not specified")        if not self.model:        """Get the base queryset."""    def get_queryset(self) -> QuerySet[T]:        }            'statuses': self.get_statuses()            'aspects': self.get_aspects(),            'mechanisms': self.get_mechanisms(),        return {        """Get all filter options."""    def get_filter_options(self) -> Dict[str, List[str]]:        ).distinct())            flat=True            'status',        return list(self.get_queryset().values_list(
