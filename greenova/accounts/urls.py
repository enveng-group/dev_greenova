from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import AccountLoginForm


class CustomLoginView(auth_views.LoginView):
    form_class = AccountLoginForm
    template_name = "accounts/pages/login.html"
    redirect_authenticated_user = True


app_name = "accounts"

urlpatterns = [
    path(
        "login/", views.CustomLoginView.as_view(), name="login"
    ),  # Add login URL
    path("register/", views.register, name="register"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # Add password reset URLs
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/pages/password_reset.html",
            email_template_name="accounts/email/password_reset_email.html",
            success_url="/accounts/password_reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/pages/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "/reset/<str:uidb64>/<str:token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/pages/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/pages/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
