from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('dashboard:home')  # Change this to redirect to dashboard

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        next_url = self.request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return response

@method_decorator(require_http_methods(['POST']), name='dispatch')
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('landing:home')
    template_name = 'authentication/logout.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return super().dispatch(request, *args, **kwargs)
        return redirect('dashboard:home')
