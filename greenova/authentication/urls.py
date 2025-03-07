from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),

    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # Update this line to use the class directly
    path('register/', views.RegisterView.as_view(), name='register'),

    # Password reset URLs remain unchanged
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
]
