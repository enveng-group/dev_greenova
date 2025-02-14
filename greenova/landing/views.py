from typing import Any, Dict
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    """Landing page view."""
    template_name = 'landing/index.html'
    
    def get(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        """Redirect authenticated users to dashboard."""
        if request.user.is_authenticated:
            return redirect(reverse('dashboard:home'))
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add landing page context data."""
        try:
            context = super().get_context_data(**kwargs)
            context.update({
                'title': 'Welcome to Greenova',
                'description': 'Environmental Management System',
                'features': [
                    {
                        'title': 'Obligation Tracking',
                        'description': 'Monitor and manage environmental obligations'
                    },
                    {
                        'title': 'Compliance Dashboard',
                        'description': 'Real-time insights into compliance status'
                    },
                    {
                        'title': 'Automated Reporting',
                        'description': 'Generate comprehensive reports easily'
                    }
                ]
            })
            logger.info("Landing page context loaded")
            return context
        except Exception as e:
            logger.error(f"Landing page error: {str(e)}")
            raise