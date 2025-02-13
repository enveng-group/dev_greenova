from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.views.generic import View
from django.db.models import QuerySet
from django.views.generic.detail import SingleObjectMixin
from .logger import logger

class LoggedActionMixin(LoginRequiredMixin, View):
    """Mixin to add logging to view actions."""
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.method:
            raise ValueError("Request method is required")
            
        action_name = f"{self.__class__.__name__}.{request.method.lower()}"
        logger.info(f"Starting {action_name}")
        try:
            response = super().dispatch(request, *args, **kwargs)
            logger.info(f"Completed {action_name}")
            return response
        except Exception as e:
            logger.error(f"Error in {action_name}: {str(e)}")
            raise

class ProjectContextMixin(SingleObjectMixin):
    """Mixin to add project-related context data."""
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            # Add common project data to context
            obj = getattr(self, 'object', None)
            if obj is not None and hasattr(obj, 'obligations'):
                context['project'] = obj
                obligations: QuerySet[Any] = obj.obligations.all()
                context['obligations'] = obligations
        except Exception as e:
            logger.error(f"Error getting project context: {str(e)}")
            raise
        return context