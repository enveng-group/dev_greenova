from typing import Any, Dict, Optional, cast, TypedDict
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpRequest
from django.core.handlers.wsgi import WSGIRequest
from .forms import GreenovaUserCreationForm  # Import the custom form
import logging

logger = logging.getLogger(__name__)

class AuthContext(TypedDict):
    form: UserCreationForm
    next: Optional[str]
    error: Optional[str]

class RegisterView(CreateView):
    form_class = GreenovaUserCreationForm
    template_name = 'authentication/auth/register.html'
    success_url = reverse_lazy('dashboard:home')

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('next'):
            context['next'] = self.request.GET['next']
        return context

    def form_valid(self, form: Any) -> HttpResponse:
        try:
            logger.info(f"New user registration: {form.cleaned_data['username']}")
            response = super().form_valid(form)
            user = form.save()
            login(self.request, user)
            next_url = self.request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return response
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            raise

@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class CustomLogoutView(LogoutView):
    """Custom logout view that handles both regular and HTMX requests."""
    template_name = 'authentication/auth/logout.html'
    next_page = reverse_lazy('landing:home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.next_page)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests - show logout confirmation page."""
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        return redirect(self.next_page)

    def post(self, request: WSGIRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle POST requests - perform logout."""
        try:
            # Perform logout
            response = super().post(request, *args, **kwargs)

            # Check if this is an HTMX request
            if request.headers.get('HX-Request'):
                return HttpResponse(
                    status=200,
                    headers={
                        'HX-Redirect': str(self.get_next_page())
                    }
                )

            return response

        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            if request.headers.get('HX-Request'):
                return HttpResponse(
                    "Logout failed",
                    status=500
                )
            raise

    def get_next_page(self) -> str:
        """Get the URL to redirect to after logout."""
        return str(self.next_page)

class HomeView(TemplateView):
    """Landing page view."""
    template_name = 'landing/index.html'

    def get(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
