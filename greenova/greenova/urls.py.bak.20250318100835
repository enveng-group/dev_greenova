from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from typing import List, Union
from django.urls.resolvers import URLPattern, URLResolver
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponseRedirect, HttpResponsePermanentRedirect
import logging
from debug_toolbar.toolbar import debug_toolbar_urls

logger = logging.getLogger(__name__)

def home_router(request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:
    """Route to appropriate home page based on auth status."""
    logger.debug(f"Home router - User authenticated: {request.user.is_authenticated}")

    # If user is not authenticated, always go to landing page
    if not request.user.is_authenticated:
        logger.info("Unauthenticated user - redirecting to landing page")
        return redirect('landing:home')

    # Only redirect to dashboard if authenticated
    logger.info("Authenticated user - redirecting to dashboard")
    return redirect('dashboard:home')

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path("__reload__/", include("django_browser_reload.urls")),
    # Landing page should be first to take precedence
    path('', home_router, name='home'),
    path('landing/', include('landing.urls')),
    path('admin/', admin.site.urls),

    # Authentication URLs
    path('authentication/', include('allauth.urls')),
    path('dashboard/', include('dashboard.urls', namespace="dashboard")),
    path('users/', include('users.urls', namespace="users")),
    path('projects/', include('projects.urls')),
    path('obligations/', include('obligations.urls')),
    path('chat/', include('chatbot.urls')),
    path('mechanisms/', include('mechanisms.urls')),
    path('procedures/', include('procedures.urls')),
    # Add company URLs
    path('company/', include('company.urls', namespace="company")),
    # Add responsibility URLs - create a new file for this
    path('responsibility/', include('responsibility.urls')),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
