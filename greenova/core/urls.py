from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'core'

urlpatterns = [
    path('health/', views.HealthCheckView.as_view(), name='health_check'),
    # Error pages for testing/development
    path('error/400/', TemplateView.as_view(template_name='errors/400.html'), name='error_400'),
    path('error/403/', TemplateView.as_view(template_name='errors/403.html'), name='error_403'),
    path('error/404/', TemplateView.as_view(template_name='errors/404.html'), name='error_404'),
    path('error/500/', TemplateView.as_view(template_name='errors/500.html'), name='error_500'),
]
