from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from .forms import AccountRegistrationForm, UserProfileForm


@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    if request.method == "POST":
        form = AccountRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Registration successful! Please log in."
            )
            return redirect("accounts:login")
    else:
        form = AccountRegistrationForm()

    return render(request, "accounts/pages/register.html", {"form": form})


@login_required
def settings(request):
    return render(request, 'accounts/pages/settings.html')


class CustomLoginView(LoginView):
    template_name = 'accounts/pages/login.html'  # Updated path
    success_url = reverse_lazy('dashboard:index')
    next_page = reverse_lazy('dashboard:index')

    def get_success_url(self):
        return str(self.success_url)


class RegisterView(TemplateView):
    template_name = "accounts/login.html"


class ProfileView(TemplateView):
    template_name = "accounts/profile.html"


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('accounts:profile_edit')
    else:
        form = UserProfileForm(instance=request.user.profile)

    return render(
        request,
        'accounts/pages/profile_edit.html',
        {'form': form, 'user': request.user},
    )
