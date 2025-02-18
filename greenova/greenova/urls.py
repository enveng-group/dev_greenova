from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from typing import List, Union
from django.urls.resolvers import URLPattern, URLResolver
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def home_router(request):
    """Route to appropriate home page based on auth status."""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return redirect('landing:home')

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path('', home_router, name='home'),
    path('admin/', admin.site.urls),
    path('landing/', include('landing.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('projects/', include('projects.urls')),
    path('analytics/', include('analytics.urls')),
    path('auth/', include('authentication.urls')),
    path('obligations/', include('obligations.urls')),
    path('chat/', include('chatbot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)