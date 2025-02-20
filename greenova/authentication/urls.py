from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLogoutView

app_name = 'authentication'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='authentication/auth/login.html'
    ), name='login'),
    
    path('logout/', CustomLogoutView.as_view(
        template_name='authentication/auth/logout.html'
    ), name='logout'),
    
    path('register/', views.RegisterView.as_view(
        template_name='authentication/auth/register.html'
    ), name='register'),
    
    # Password reset URLs
    path('password/reset/', auth_views.PasswordResetView.as_view(
        template_name='authentication/password/reset/form.html',
        email_template_name='authentication/password/email/reset.html',
        subject_template_name='authentication/password/email/subject.txt'
    ), name='password_reset'),
    
    path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='authentication/password/reset/done.html'
    ), name='password_reset_done'),
    
    path('password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='authentication/password/reset/confirm.html'
    ), name='password_reset_confirm'),
    
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='authentication/password/reset/complete.html'
    ), name='password_reset_complete'),
    
    path('validate/username/', views.ValidateUsernameView.as_view(), 
         name='validate_username'),
]