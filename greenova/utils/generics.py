from typing import Any, Dict, List, TypeVar, Generic, cast, Type
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Model
from django.http import HttpRequest

# Local imports with absolute paths
from greenova.utils.mixins import LoggedActionMixin
from greenova.utils.actions import AnalyticsActions
from greenova.utils.pagination import ProjectPagination
from greenova.utils.error_handlers import handle_error
from greenova.obligations.models import Obligation
from greenova.obligations.filters import ObligationFilter
from greenova.utils.django_type_safety import TypedModelAdmin

T = TypeVar('T', bound=Model)

class BaseAnalyticsView(LoggedActionMixin, LoginRequiredMixin, Generic[T], TemplateView):
    """Base class for analytics views with type safety."""
    model: Type[T]
    request: HttpRequest

    def get_queryset(self) -> QuerySet[T]:
        """Get the base queryset with type safety."""
        if not hasattr(self, 'model') or not self.model:
            raise ValueError("Model not specified")
        return self.model.objects.all()


@handle_error
class AnalyticsView(BaseAnalyticsView[T]):
    """Analytics view implementation with proper type hints."""

    actions: AnalyticsActions = AnalyticsActions()

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add common analytics context data with type safety."""
        context = super().get_context_data(**kwargs)
        try:
            queryset: QuerySet[T] = self.get_queryset()

            # Add pagination
            paginator = ProjectPagination(queryset)
            page = self.request.GET.get('page', '1')
            context['page_obj'] = paginator.get_page(int(page))

            # Add filtering with proper type checking
            if queryset.exists():
                first_item = queryset.first()
                if isinstance(first_item, Obligation):
                    obligation_filter = ObligationFilter(cast(QuerySet[Obligation], queryset))
                    status = self.request.GET.get('status')
                    if status:
                        filtered_qs = obligation_filter.filter_by_status(status)
                        queryset = cast(QuerySet[T], filtered_qs)

            context['queryset'] = queryset
            context['metrics'] = self.actions.calculate_metrics(queryset)
            context['filter_options'] = self.get_filter_options()
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
        """Get list of mechanisms with proper type conversion."""
        queryset = self.get_queryset()
        return list(
            queryset.values_list('primary_environmental_mechanism', flat=True)
            .distinct()
            .order_by('primary_environmental_mechanism')
        )

    def get_aspects(self) -> List[str]:
        """Get list of aspects with proper type conversion."""
        queryset = self.get_queryset()
        return list(
            queryset.values_list('environmental_aspect', flat=True)
            .distinct()
            .order_by('environmental_aspect')
        )

    def get_statuses(self) -> List[str]:
        """Get list of statuses with proper type conversion."""
        queryset = self.get_queryset()
        return list(
            queryset.values_list('status', flat=True)
            .distinct()
            .order_by('status')
        )

    def get_filter_options(self) -> Dict[str, List[str]]:
        """Get all filter options."""
        return {
            'mechanisms': self.get_mechanisms(),
            'aspects': self.get_aspects(),
            'statuses': self.get_statuses()
        }
