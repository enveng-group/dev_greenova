from typing import Any, Dict, Optional, cast, TypedDict
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.core.handlers.wsgi import WSGIRequest
from .forms import GreenovaUserCreationForm
import logging
from django_htmx.http import trigger_client_event

logger = logging.getLogger(__name__)

class AuthContext(TypedDict):
    form: UserCreationForm
    next: Optional[str]
    error: Optional[str]

class RegisterView(CreateView):
    form_class = GreenovaUserCreationForm
    template_name = 'authentication/auth/register.html'
    success_url = reverse_lazy('dashboard:home')

    def get_context_data(self, **kwargs: Dict[str, Any]) -> AuthContext:
        context = cast(AuthContext, super().get_context_data(**kwargs))
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

    def form_invalid(self, form: Any) -> HttpResponse:
        """Handle invalid form submission with HTMX support."""
        if self.request.headers.get('HX-Request'):
            return HttpResponse(
                self.render_to_string('authentication/components/messages/form_errors.html', 
                {'form': form}),
                status=422
            )
        return super().form_invalid(form)

    def render_to_string(self, template: str, context: Dict[str, Any]) -> str:
        """Helper method to render template strings."""
        from django.template.loader import render_to_string
        return render_to_string(template, context, request=self.request)

@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class CustomLogoutView(LogoutView):
    """Custom logout view that handles both regular and HTMX requests."""
    template_name = 'authentication/auth/logout.html'
    next_page = reverse_lazy('landing:home')
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests - show logout confirmation page."""
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        return redirect(self.next_page)
    def post(self, request: WSGIRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle POST requests - perform logout."""
        try:
            response = super().post(request, *args, **kwargs)
            
            # Check if this is an HTMX request
            if request.headers.get('HX-Request'):
                return JsonResponse({
                    'success': True,
                    'redirect_url': str(self.next_page)
                }, headers={
                    'HX-Redirect': str(self.next_page)
                })
            
            return response
            
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            if request.headers.get('HX-Request'):
                return JsonResponse({
                    'success': False,
                    'error': 'Logout failed'
                }, status=500)
            raise

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

class ValidateUsernameView(View):
    """Handle real-time username validation."""
    
    def get(self, request: HttpRequest) -> HttpResponse:
        """Check username availability."""
        username = request.GET.get('username', '')
        is_taken = User.objects.filter(username=username).exists()
        
        if is_taken:
            return HttpResponse(
                '<small class="error">Username is already taken</small>',
                status=422
            )
        return HttpResponse(
            '<small class="success">Username is available</small>'
        )
