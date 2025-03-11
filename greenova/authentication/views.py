from typing import Any, cast, Dict, Optional, TypedDict
from django.contrib.auth import login, logout as auth_logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.cache import cache_control
from django_htmx.http import (
    HttpResponseClientRedirect,
    trigger_client_event,
    push_url
)
from .forms import GreenovaUserCreationForm
import logging

logger = logging.getLogger(__name__)

class AuthContext(TypedDict):
    form: UserCreationForm
    next: Optional[str]
    error: Optional[str]

@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
@method_decorator(vary_on_headers("HX-Request"), name='dispatch')
class CustomLoginView(UserPassesTestMixin, LoginView):
    """Custom login view that extends Django's LoginView."""
    next_page = reverse_lazy('dashboard:home')
    template_name = 'authentication/auth/login.html'

    def test_func(self) -> bool:
        """
        Prevent logged-in users from accessing login page.
        """
        return not self.request.user.is_authenticated

    def handle_no_permission(self) -> HttpResponseRedirect:
        """
        Redirect authenticated users to the home page.
        """
        return HttpResponseRedirect(str(self.next_page))

    def form_valid(self, form):
        """Process valid form data."""
        response = super().form_valid(form)

        # If using HTMX, use client-side redirect for better UX
        if self.request.htmx:
            redirect_url = self.get_success_url()
            return HttpResponseClientRedirect(redirect_url)

        return response

    def form_invalid(self, form):
        """Process invalid form data."""
        response = super().form_invalid(form)

        # If using HTMX, trigger client-side validation errors
        if self.request.htmx:
            trigger_client_event(response, 'loginValidationFailed',
                                params={'errors': form.errors})

        return response

@method_decorator(vary_on_headers("HX-Request"), name='dispatch')
class CustomLogoutView(LogoutView):
    """Custom logout view that extends Django's LogoutView."""
    next_page = reverse_lazy('landing:home')
    template_name = 'authentication/auth/logout.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle both GET and POST requests for logout."""
        response = super().dispatch(request, *args, **kwargs)

        # If using HTMX, use client-side redirect
        if request.htmx:
            return HttpResponseClientRedirect(str(self.next_page))

        return response

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle POST requests."""
        auth_logout(request)

        if request.htmx:
            return HttpResponseClientRedirect(str(self.next_page))
        return HttpResponseRedirect(str(self.next_page))

@method_decorator(vary_on_headers("HX-Request"), name='dispatch')
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

            # Determine redirect URL
            next_url = self.request.GET.get('next', self.success_url)

            # If HTMX request, use client-side redirect
            if self.request.htmx:
                return HttpResponseClientRedirect(next_url)

            # Standard redirect for non-HTMX requests
            if next_url:
                return redirect(next_url)
            return response

        except Exception as e:
            logger.error(f"Registration error: {str(e)}")

            # If HTMX, return error with event trigger
            if self.request.htmx:
                response = HttpResponse(status=500)
                trigger_client_event(response, 'registrationError',
                                    params={'error': str(e)})
                return response
            raise
