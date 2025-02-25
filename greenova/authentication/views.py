from typing import Any, Dict, Optional, TypedDict
from django.contrib.auth import login, logout as auth_logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from .forms import GreenovaUserCreationForm
import logging

logger = logging.getLogger(__name__)

class AuthContext(TypedDict):
    form: UserCreationForm
    next: Optional[str]
    error: Optional[str]

@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class CustomLogoutView(LogoutView):
    """Custom logout view that extends Django's LogoutView."""
    next_page = reverse_lazy('landing:home')
    template_name = 'authentication/auth/logout.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle both GET and POST requests for logout."""
        response = super().dispatch(request, *args, **kwargs)

        # Check if request is HTMX
        if request.headers.get('HX-Request'):
            return HttpResponseRedirect(str(self.next_page))

        return response

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle POST requests."""
        auth_logout(request)
        return HttpResponseRedirect(str(self.next_page))

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
