from typing import Any, Dict, List, TypeVar, Generic
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Model
from utils.mixins import LoggedActionMixin
from .actions import AnalyticsActions

T = TypeVar('T', bound=Model)

class AnalyticsView(LoggedActionMixin, LoginRequiredMixin, Generic[T], TemplateView):
    """Base view for analytics pages."""
    
    actions: AnalyticsActions = AnalyticsActions()
    model: type[T]

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add common analytics context data."""
        context = super().get_context_data(**kwargs)
        try:
            queryset = self.get_queryset()
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
        return list(self.get_queryset().values_list(
            'status',
            flat=True
        ).distinct())

    def get_filter_options(self) -> Dict[str, List[str]]:
        """Get all filter options."""
        return {
            'mechanisms': self.get_mechanisms(),
            'aspects': self.get_aspects(),
            'statuses': self.get_statuses()
        }

    def get_queryset(self) -> QuerySet[T]:
        """Get the base queryset."""
        if not self.model:
            raise ValueError("Model not specified")
        return self.model.objects.all()