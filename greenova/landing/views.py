from typing import Any, Dict
from django.views.generic import TemplateView
from django_htmx.http import trigger_client_event
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    """Landing page view."""
    template_name = 'landing/index.html'
    
    def get(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        """Handle GET requests with HTMX support."""
        if request.htmx:  # New HTMX property from middleware
            # Return partial template for HTMX requests
            context = self.get_context_data(**kwargs)
            return HttpResponse(
                self.render_to_string('landing/partials/features.html', context)
            )
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Add landing page context data."""
        context = super().get_context_data(**kwargs)
        # Add show_landing_content flag
        context['show_landing_content'] = True
        # Still add dashboard link if authenticated
        if self.request.user.is_authenticated:
            context['show_dashboard_link'] = True
        return context

    def render_to_string(self, template, context):
        """Helper method to render template strings."""
        from django.template.loader import render_to_string
        return render_to_string(template, context, request=self.request)