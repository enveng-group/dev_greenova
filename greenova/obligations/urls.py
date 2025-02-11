from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'obligations'

urlpatterns = [
    # Authentication URLs
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='obligations/login.html'),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='obligations:login'),
        name='logout',
    ),
    # Password Reset URLs
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='obligations/password_reset.html'
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='obligations/password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='obligations/password_reset_confirm.html'
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='obligations/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    # Obligation CRUD URLs
    path('', views.ObligationListView.as_view(), name='list'),
    path(
        'obligation/<str:pk>/',
        views.ObligationDetailView.as_view(),
        name='detail',
    ),
    path(
        'obligation/create/',
        views.ObligationCreateView.as_view(),
        name='create',
    ),
    path(
        'obligation/<str:pk>/edit/',
        views.ObligationUpdateView.as_view(),
        name='edit',
    ),
    path(
        'obligation/<str:pk>/delete/',
        views.ObligationDeleteView.as_view(),
        name='delete',
    ),
    # Import/Export URLs
    path('import/', views.import_obligations, name='import'),
    path('export/', views.export_obligations, name='export'),
]
