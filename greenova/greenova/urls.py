from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

def home_router(request):
    """Redirect all traffic to admin login page"""
    return redirect('admin:index')

urlpatterns = [
    # Redirect root URL to admin
    path('', home_router, name='home'),

    # Admin URL - this is the main access point for users
    path('admin/', admin.site.urls),

]
