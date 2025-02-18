from typing import Any, Dict
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.http import HttpRequest, HttpResponse
import logging

logger = logging.getLogger(__name__)

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'authentication/auth/register.html'
    success_url = reverse_lazy('dashboard:home')

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

@method_decorator(require_http_methods(['POST']), name='dispatch')
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('landing:home')
    template_name = 'authentication/auth/logout.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]) -> HttpResponse:
        if request.method == 'POST':
            return super().dispatch(request, *args, **kwargs)
        return redirect('dashboard:home')

from django.views.generic import TemplateView
from django.urls import reverse
from utils.mixins import NavigationMixin

class HomeView(NavigationMixin, TemplateView):
    """Landing page view."""
    template_name = 'landing/index.html'
    
    def get(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
